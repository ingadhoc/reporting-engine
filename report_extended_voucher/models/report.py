# -*- coding: utf-8 -*-
from openerp import models, fields


class ir_actions_report(models.Model):
    _inherit = 'ir.actions.report.xml'

    receiptbook_ids = fields.Many2many(
        'account.voucher.receiptbook',
        'report_configuration_receiptbook_relation',
        'report_configuration_id',
        'receiptbook_id',
        'ReceiptBooks',
        )
    voucher_type = fields.Selection(
        [('payment', 'Payment'), ('receipt', 'Receipt')], 'Voucher Type', )

    def get_domains(self, cr, model, record, context=None):
        domains = super(ir_actions_report, self).get_domains(
            cr, model, record, context=context)
        if model == 'account.voucher':
            # Search for especific report
            domains.append([
                ('voucher_type', '=', record.type),
                ('receiptbook_ids', '=', record.receiptbook_id.id)])

            # Search without type
            domains.append([
                ('voucher_type', '=', False),
                ('receiptbook_ids', '=', record.receiptbook_id.id)])

            # Search without journal and with type
            domains.append([
                ('voucher_type', '=', record.type),
                ('receiptbook_ids', '=', False)])

            # Search without journal and without type
            domains.append([
                ('voucher_type', '=', False),
                ('receiptbook_ids', '=', False)])
        return domains
