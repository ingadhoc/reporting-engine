##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_report(self):
        """Para ser usado tmb, por ejemplo, desde qweb en website_portal
        """
        return self.env['ir.actions.report'].get_report(self)

    def action_invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        if any(not move.is_invoice(include_receipts=True) for move in self):
            raise UserError(_("Only invoices could be printed."))

        self.filtered(lambda inv: not inv.invoice_sent).write({'invoice_sent': True})
        # if we print caming from other model then active id and active model
        # is wrong and it raise an error with custom filename
        self = self.with_context(
            active_model=self._name, active_id=self.id, active_ids=self.ids)
        report_name = self.get_report().report_name
        return self.env['ir.actions.report'].search(
            [('report_name', '=', report_name)], limit=1).report_action(self)
