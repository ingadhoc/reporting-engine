##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    account_invoice_state = fields.Selection(
        [('proforma', 'Pro-forma'), ('approved_invoice', 'Aproved Invoice')],
        'Invoice State', required=False)
    account_invoice_journal_ids = fields.Many2many(
        'account.journal', 'report_account_journal_rel', 'report_id',
        'journal_id', 'Journals',
        domain=[('type', 'in', ['sale', 'sale_refund'])])
    account_invoice_split_invoice = fields.Boolean(
        'Split Inovice',
        help='If true, when validating the invoice, if it contains more than '
        'the specified number of lines, new invoices will be generated.')
    account_invoice_lines_to_split = fields.Integer(
        'Lines to split')
    document_type_ids = fields.Many2many(
        'account.document.type', 'report_account_document_type_rel',
        'report_id', 'document_type_id',
        string='Document Types',
    )

    def get_domains(self, record):
        domains = super(IrActionsReport, self).get_domains(record)
        if record._name == 'account.invoice':
            account_invoice_state = False

            # TODO we should improove this

            # We use ignore_state to get the report to split invoice before
            # the invoice is validated
            ignore_state = self._context.get('ignore_state', False)
            if ignore_state:
                account_invoice_state = ['approved_invoice', 'proforma', False]
            elif record.state in ['proforma', 'proforma2']:
                account_invoice_state = ['proforma']
            elif record.state in ['open', 'paid', 'sale']:
                account_invoice_state = ['approved_invoice']
            # Search for especific state and document type and journal
            domains.append([
                ('account_invoice_state', 'in', account_invoice_state),
                ('account_invoice_journal_ids', '=', record.journal_id.id),
                ('document_type_ids', '=',
                    record.document_type_id.id)])

            # Search for especific state and document type without journal
            domains.append([
                ('account_invoice_state', 'in', account_invoice_state),
                ('account_invoice_journal_ids', '=', False),
                ('document_type_ids', '=',
                    record.document_type_id.id)])

            # Search for especific state and journal without document type
            domains.append([
                ('account_invoice_state', 'in', account_invoice_state),
                ('account_invoice_journal_ids', '=', record.journal_id.id),
                ('document_type_ids', '=', False)])

            # Search for especific document type and journal without state
            domains.append([
                ('account_invoice_state', '=', False),
                ('account_invoice_journal_ids', '=', record.journal_id.id),
                ('document_type_ids', '=',
                    record.document_type_id.id)])

            # Search for especific document type without state and journal
            domains.append([
                ('account_invoice_state', '=', False),
                ('account_invoice_journal_ids', '=', False),
                ('document_type_ids', '=',
                    record.document_type_id.id)])

            # Search for especific journal without state and document type
            domains.append([
                ('account_invoice_state', '=', False),
                ('account_invoice_journal_ids', '=', record.journal_id.id),
                ('document_type_ids', '=', False)])

            # Search for especific document type without journal and
            # without state
            domains.append([
                ('account_invoice_state', '=', False),
                ('account_invoice_journal_ids', '=', False),
                ('document_type_ids', '=',
                    record.document_type_id.id)])

            # Search without journal, state and document type
            domains.append([
                ('account_invoice_state', '=', False),
                ('account_invoice_journal_ids', '=', False),
                ('document_type_ids', '=', False)])

        return domains

    @api.multi
    def _extend_report_context(self, docids, data=None):
        self = super(
            IrActionsReport, self)._extend_report_context(
            docids, data=data)

        if self._context.get('active_model') == 'account.invoice' and\
                'active_id' in self._context:
            active_object = self.env[self._context['active_model']].browse(
                self._context['active_id'])
            report_partner = active_object.journal_id.report_partner_id
            if report_partner:
                temp_company = self.env['res.company'].new(
                    {'partner_id': report_partner.id})
                self = self.with_context(company=temp_company)
                if self.print_logo == 'company_logo':
                    self = self.with_context(logo_report=report_partner.image)
        return self
