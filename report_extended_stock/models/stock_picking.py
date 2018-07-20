##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def do_print_picking(self):
        '''This function prints the picking list'''
        self.ensure_one()

        self.write({'printed': True})
        # if we print caming from other model then active id and active model
        # is wrong and it raise an error with custom filename
        self = self.with_context(
            active_model=self._name, active_id=self.id, active_ids=self.ids,
            stock_report_type='picking_list')

        return self.env['ir.actions.report'].get_report(self).report_action(
            self)

    @api.multi
    def do_print_voucher(self):
        '''This function prints the voucher (deliveryslip)'''
        self.ensure_one()

        # if we print caming from other model then active id and active model
        # is wrong and it raise an error with custom filename
        self = self.with_context(
            active_model=self._name, active_id=self.id, active_ids=self.ids,
            stock_report_type='voucher')

        return self.env['ir.actions.report'].get_report(self).report_action(
            self)

    @api.multi
    @api.constrains('sale_id')
    def set_notes(self):
        """Setamos notas internas y observaciones desde la venta
        """
        for rec in self.filtered('sale_id'):
            vals = {}
            if rec.sale_id.internal_notes:
                vals['note'] = rec.sale_id.internal_notes
            if rec.sale_id.note:
                vals['observations'] = rec.sale_id.note
            rec.update(vals)
