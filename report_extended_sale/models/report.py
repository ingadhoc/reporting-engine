##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    sale_order_state = fields.Selection(
        [('draft', 'Quotation'), ('progress', 'In Progress')],
        'Sale Order State', required=False)

    def get_domains(self, record):
        domains = super(IrActionsReport, self).get_domains(record)
        if record.state in ['draft', 'sent']:
            sale_order_state = 'draft'
        else:
            sale_order_state = 'progress'
        if record._name == 'sale.order':
            # Search for especific report
            domains.append([('sale_order_state', '=', sale_order_state)])
            # Search without state defined
            domains.append([('sale_order_state', '=', False)])
        return domains

    @api.multi
    def _extend_report_context(self, docids, data=None):
        self = super(
            IrActionsReport, self)._extend_report_context(
            docids, data=data)

        if self._context.get('active_model') == 'sale.order' and\
                'active_id' in self._context:
            active_object = self.env[self._context['active_model']].browse(
                self._context['active_id'])
            report_partner = active_object.sale_checkbook_id.report_partner_id
            if report_partner:
                temp_company = self.env['res.company'].new(
                    {'partner_id': report_partner.id})
                self = self.with_context(company=temp_company)
                if self.print_logo == 'company_logo':
                    self = self.with_context(logo_report=report_partner.image)
        return self
