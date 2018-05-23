##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import UserError
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
    def get_report_name(self, model, model_ids):
        report = self.get_report(model, model_ids)
        return report.report_name

    @api.model
    def get_report(self, model, model_ids):
        records = self.env[model].browse(model_ids)
        domains = self.get_domains(model, records[0])

        # TODO habria que mejorar esto porque se podria recibir un listado de
        # ids con distintas cias
        if hasattr(
                records, 'company_id') and records[0].company_id:
            company = records.company_id
        else:
            company = self.env['res.users'].browse(
                uid).company_id
        for domain in domains:
            domain.append(('model', '=', model))

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
            raise UserError(_(title, message))
        return report

    @api.model
    def get_domains(self, model, record):
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

    @api.model
    def render_qweb_html(self, docids, data=None):
        # TODO mejorar este metodo para que sea "heredado"
        """This method generates and returns html version of a report.
        """
        # If the report is using a custom model to render its html, we must use
        # it.
        # Otherwise, fallback on the generic html rendering.
        if data is None:
            data = {}

        # report_model_name = 'report.%s' % self.report_name
        # report_model = self.env.get(report_model_name)
        # report = self._get_report_from_name()
        report = self

        # We add all the key-value pairs of the report configuration
        for report_conf_line in report.line_ids:
            if report_conf_line.value_type == 'text':
                data.update(
                    {report_conf_line.name: report_conf_line.value_text})
            elif report_conf_line.value_type == 'boolean':
                data.update(
                    {report_conf_line.name: (
                        report_conf_line.value_boolean)})
        data.update({
            'report': report,
            'to_word': to_word,
        })
        return super(IrActionsReport, self).render_qweb_html(docids, data=data)
