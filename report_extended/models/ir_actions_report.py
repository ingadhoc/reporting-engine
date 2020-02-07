##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import tools, models, fields, api, _
from odoo.exceptions import UserError
import datetime

from . import conversor


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    sequence = fields.Integer(
        'Sequence',
        help="Used to order priority of reports",
        default=10,
    )
    line_ids = fields.One2many(
        'report.configuration.line',
        'report_id',
        string='Configuration lines'
    )
    print_logo = fields.Selection([
        ('no_logo', 'Do not print log'),
        ('company_logo', 'Company Logo'),
        ('specified_logo', 'Specified Logo')],
        'Print Logo',
        required=True,
        default='no_logo',
    )
    logo = fields.Binary(
        'Logo'
    )
    use_background_image = fields.Boolean(
        'Use Background Image'
    )
    background_image = fields.Binary(
        'Background Image'
    )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        change_default=True,
    )

    @api.model
    def get_report(self, records):
        domains = self.get_domains(records[0])

        # TODO habria que mejorar esto porque se podria recibir un listado de
        # ids con distintas cias
        if hasattr(
                records, 'company_id') and records[0].company_id:
            company = records.company_id
        else:
            company = self.env.user.company_id
        for domain in domains:
            domain.append(('model', '=', records[0]._name))

            # Search for company specific
            domain_with_company = domain + [('company_id', '=', company.id)]
            reports = self.search(domain_with_company, order='sequence')
            if reports:
                break

            # If not company specific, then for any company (allowed to the
            # user)
            reports = self.search(domain, order='sequence')
            if reports:
                break
        if reports:
            report = reports[0]
        else:
            title = _('No report defined')
            message = _('There is no report defined for this conditions.')
            raise UserError(title + '. ' + message)
        return report

    @api.model
    def get_domains(self, record):
        return []

    @api.multi
    def update_lines_that_apply(self):
        config_defaults = self.env['report.configuration.default'].search([])
        for report in self:
            conf_line_name_id = {}
            for line in report.line_ids:
                conf_line_name_id[line.name] = line

            for key_value in config_defaults:
                if (
                        key_value.apply_to_all or
                        key_value.apply_to_model_id.model == report.model):
                    vals = {'name': key_value.name, 'report_id': report.id}
                    if key_value.value_type == 'text':
                        vals['value_type'] = 'text'
                        vals['value_text'] = key_value.value_text
                    elif key_value.value_type == 'boolean':
                        vals['value_type'] = 'boolean'
                        vals['value_boolean'] = key_value.value_boolean

                    if conf_line_name_id.get(key_value.name, False):
                        if key_value.override_values:
                            conf_line_name_id[key_value.name].write(vals)
                    else:
                        self.env['report.configuration.line'].create(vals)

    @api.model
    def create(self, vals):
        '''
        When a Report is created, we add the default keys.
        '''
        rec = super(IrActionsReport, self).create(vals)
        no_key_lines = self._context.get('no_key_lines', False)
        if not no_key_lines:
            rec.update_lines_that_apply()
        return rec

    @api.multi
    def _extend_report_context(self, docids, data=None):
        company = self.env.user.company_id
        # if we have company on the active object we prefer it (odoo does
        # similar on web external_layout)
        recs = self.env.get(self.model).browse(docids)
        if recs and 'company_id' in recs._fields and recs[0].company_id:
            company = recs[0].company_id

        # We add logo
        print_logo = False
        if self.print_logo == 'specified_logo':
            print_logo = self.logo
        elif self.print_logo == 'company_logo':
            if company.logo:
                print_logo = company.logo

        # We add all the key-value pairs of the report configuration
        # We add keys so that you can use it in a safe way in reports
        # (like keys.get('key name'))
        keys = {}
        context_update = {}
        for report_conf_line in self.line_ids:
            key_value = report_conf_line.value_type == 'text' and \
                report_conf_line.value_text or report_conf_line.value_boolean
            context_update[report_conf_line.name] = key_value
            keys[report_conf_line.name] = key_value

        context_update.update({
            'keys': keys,
            'use_background_image': self.use_background_image,
            'logo_report': print_logo,
            'background_image': self.use_background_image and
            self.background_image,
            'number_to_string': conversor.to_word,
            'partner_address': self.partner_address,
            'net_price': self.net_price,
            'datetime': datetime,
            'tools': tools,
            'company': company,
        })
        return self.with_context(**context_update)

    def net_price(self, gross_price, discount):
        return gross_price * (1 - (discount / 100))

    def partner_address(self, partner):
        # TODO use odoo native fomat address function
        ret = ''
        if partner.street:
            ret += partner.street
        if partner.street2:
            if partner.street:
                ret += ' - ' + partner.street2
            else:
                ret += partner.street2
        if ret != '':
            ret += '. '

        if partner.zip:
            ret += '(' + partner.zip + ')'
        if partner.city:
            if partner.zip:
                ret += ' ' + partner.city
            else:
                ret += partner.city
        if partner.state_id:
            if partner.city:
                ret += ' - ' + partner.state_id.name
            else:
                ret += partner.state_id.name
        if partner.zip or partner.city or partner.state_id:
            ret += '. '

        if partner.country_id:
            ret += partner.country_id.name + '.'

        return ret

    # it should be api.multi but on odoo is defined as api.model
    @api.model
    def render_qweb_html(self, docids, data=None):
        self = self._extend_report_context(docids, data=data)
        return super(IrActionsReport, self).render_qweb_html(docids, data=data)

    @api.model
    def render_aeroo(self, docids, data=None):
        self = self._extend_report_context(docids, data=data)
        return super(IrActionsReport, self).render_aeroo(docids, data)
