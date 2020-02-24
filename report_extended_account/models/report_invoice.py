##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    account_invoice_journal_ids = fields.Many2many(
        'account.journal', 'report_account_journal_rel', 'report_id',
        'journal_id', 'Journals',
        domain=[('type', 'in', ['sale', 'sale_refund'])])
    document_type_ids = fields.Many2many(
        'l10n_latam.document.type', 'report_account_document_type_rel',
        'report_id', 'document_type_id',
        string='Document Types',
    )

    def get_domains(self, record):
        domains = super(IrActionsReport, self).get_domains(record)
        if record._name == 'account.move':

            # Search for document type and journal
            domains.append([
                ('account_invoice_journal_ids', '=', record.journal_id.id),
                ('document_type_ids', '=', record.l10n_latam_document_type_id.id)])

            # Search for document type without journal
            domains.append([
                ('account_invoice_journal_ids', '=', False),
                ('document_type_ids', '=', record.l10n_latam_document_type_id.id)])

            # Search for journal without document type
            domains.append([
                ('account_invoice_journal_ids', '=', record.journal_id.id),
                ('document_type_ids', '=', False)])

            # Search without journal and document type
            domains.append([
                ('account_invoice_journal_ids', '=', False),
                ('document_type_ids', '=', False)])

        return domains

    def _extend_report_context(self, docids, data=None):
        self = super(
            IrActionsReport, self)._extend_report_context(
            docids, data=data)

        if self._context.get('active_model') == 'account.move' and\
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
