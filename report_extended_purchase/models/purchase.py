# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    internal_notes = fields.Text('Internal Notes')

    @api.multi
    def print_quotation(self):
        self.write({'state': "sent"})
        report_name = self.env['ir.actions.report.xml'].get_report_name(
            self._name, self.ids)
        return self.env['report'].get_action(self, report_name)

    @api.model
    def _prepare_picking(self):
        res = super(PurchaseOrder, self)._prepare_picking()
        res['note'] = self.internal_notes
        return res
