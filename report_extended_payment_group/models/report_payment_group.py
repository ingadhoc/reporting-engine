from odoo import models, fields, api


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

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

    def get_domains(self, record):
        domains = super(IrActionsReport, self).get_domains(record)
        if record._name == 'account.payment.group':
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

    @api.multi
    def _extend_report_context(self, docids, data=None):
        self = super(
            IrActionsReport, self)._extend_report_context(
            docids, data=data)

        if self._context.get('active_model') == 'account.payment.group' and\
                'active_id' in self._context:
            active_object = self.env[self._context['active_model']].browse(
                self._context['active_id'])
            report_partner = active_object.receiptbook_id.report_partner_id
            if report_partner:
                temp_company = self.env['res.company'].new(
                    {'partner_id': report_partner.id})
                self = self.with_context(company=temp_company)
                if self.print_logo == 'company_logo':
                    self = self.with_context(logo_report=report_partner.image)
        return self
