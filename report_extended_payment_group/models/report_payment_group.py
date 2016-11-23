# -*- coding: utf-8 -*-
from openerp import models, fields


class ir_actions_report(models.Model):
    _inherit = 'ir.actions.report.xml'

    receiptbook_ids = fields.Many2many(
        'account.payment.receiptbook',
        'report_configuration_receiptbook_relation',
        'report_configuration_id',
        'receiptbook_id',
        'ReceiptBooks',
    )
    partner_type = fields.Selection(
        # [('inbound', 'Inbound'), ('outbound', 'Outbound')],
        [('customer', 'Customer'), ('supplier', 'Vendor')],
        # [('payment', 'Payment'), ('receipt', 'Receipt')], 'Voucher Type', )
    )

    def get_domains(self, cr, model, record, context=None):
        domains = super(ir_actions_report, self).get_domains(
            cr, model, record, context=context)
        if model == 'account.payment.group':
            # Search for especific report
            domains.append([
                ('partner_type', '=', record.partner_type),
                ('receiptbook_ids', '=', record.receiptbook_id.id)])

            # Search without type
            domains.append([
                ('partner_type', '=', False),
                ('receiptbook_ids', '=', record.receiptbook_id.id)])

            # Search without journal and with type
            domains.append([
                ('partner_type', '=', record.partner_type),
                ('receiptbook_ids', '=', False)])

            # Search without journal and without type
            domains.append([
                ('partner_type', '=', False),
                ('receiptbook_ids', '=', False)])
        return domains
