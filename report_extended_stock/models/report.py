##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    stock_picking_book_ids = fields.Many2many(
        'stock.book',
        'report_configuration_stock_book_rel',
        'report_configuration_id', 'book_id', 'Picking Books')
    stock_picking_type_ids = fields.Many2many(
        'stock.picking.type',
        'report_configuration_stock_picking_type_rel',
        'report_configuration_id', 'picking_type_id', 'Picking Types')
    stock_report_type = fields.Selection(
        [('voucher', 'Voucher'), ('picking_list', 'Picking List')],
        'Stock Report Type',)

    def get_domains(self, record):
        domains = super(IrActionsReport, self).get_domains(record)
        if record._name == 'stock.picking':
            stock_report_type = self._context.get('stock_report_type', False)
            if stock_report_type:
                # Search for especific picking type and report type
                domains.append([
                    ('stock_picking_type_ids', '=', record.picking_type_id.id),
                    ('stock_picking_book_ids', '=', record.book_id.id),
                    ('stock_report_type', '=', stock_report_type),
                ])
                # Search for especific report type
                domains.append([
                    ('stock_report_type', '=', stock_report_type),
                    ('stock_picking_book_ids', '=', record.book_id.id),
                ])
                domains.append([
                    ('stock_report_type', '=', stock_report_type),
                    ('stock_picking_type_ids', '=', record.picking_type_id.id),
                ])
                domains.append([
                    ('stock_report_type', '=', stock_report_type),
                ])
            # Search for especific boook and report type
            domains.append(
                [('stock_picking_book_ids', '=', record.book_id.id)])
            # Search for especific picking type and report type
            domains.append(
                [('stock_picking_type_ids', '=', record.picking_type_id.id)])
            # Search without book
            domains.append([('stock_picking_book_ids', '=', False)])
            # Search without picking_type
            domains.append([('stock_picking_type_ids', '=', False)])
            # Search without picking_type
            domains.append([('stock_report_type', '=', False)])
        return domains

    @api.multi
    def _extend_report_context(self, docids, data=None):
        self = super(
            IrActionsReport, self)._extend_report_context(
            docids, data=data)

        if self._context.get('active_model') == 'stock.picking' and\
                'active_id' in self._context:
            active_object = self.env[self._context['active_model']].browse(
                self._context['active_id'])
            report_partner = active_object.book_id.report_partner_id
            if report_partner:
                temp_company = self.env['res.company'].new(
                    {'partner_id': report_partner.id})
                self = self.with_context(company=temp_company)
                if self.print_logo == 'company_logo':
                    self = self.with_context(logo_report=report_partner.image)
        return self
