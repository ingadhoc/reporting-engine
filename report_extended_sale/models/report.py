##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


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
