# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api


class stock_picking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def do_print_picking(self):
        '''This function prints the picking list'''
        self.ensure_one()
        self.write({'printed': True})
        report_name = self.env['ir.actions.report.xml'].with_context(
            stock_report_type='picking_list').get_report_name(
            self._name, self.ids)
        return self.env['report'].get_action(self, report_name)

    @api.multi
    def do_print_voucher(self):
        '''This function prints the voucher'''
        self.ensure_one()
        self.write({'printed': True})
        # no sure why but sometimes it cames other models as activemodel
        # and it gives an error, for eg if you came from picking from sale
        # order and print is enable on picking confirmation
        self = self.with_context(active_model='stock.picking')
        report_name = self.env['ir.actions.report.xml'].with_context(
            stock_report_type='voucher').get_report_name(
            self._name, self.ids)
        report = self.env['report'].get_action(self, report_name)
        # funcionalidad depreciada
        # if self._context.get('keep_wizard_open', False):
        #     report['type'] = 'ir.actions.report_dont_close_xml'
        return report


class stock_move(models.Model):
    _inherit = 'stock.move'

    @api.cr_uid_ids_context
    def _picking_assign(self, cr, uid, move_ids, context=None):
        # TODO deberiamos mejroar esta horrible implmentacion
        res = super(stock_move, self)._picking_assign(
            cr, uid, move_ids, context=context)
        move = self.browse(cr, uid, move_ids, context=context)[0]
        pick_obj = self.pool.get("stock.picking")
        picks = pick_obj.search(cr, uid, [
            ('group_id', '=', move.group_id.id),
            ('location_id', '=', move.location_id.id),
            ('location_dest_id', '=', move.location_dest_id.id),
            ('picking_type_id', '=', move.picking_type_id.id),
            ('printed', '=', False),
            ('state', 'in', [
                'draft', 'confirmed', 'waiting',
                'partially_available', 'assigned'])], limit=1, context=context)

        vals = {}
        sale_order = move.procurement_id.sale_line_id.order_id
        if move.picking_id.company_id.internal_notes:
            vals.update({
                'note': sale_order.internal_notes})
        if move.picking_id.company_id.external_notes:
            vals.update({
                'observations': sale_order.note})
        if picks:
            pick_obj.write(cr, uid, picks, vals)

        return res
