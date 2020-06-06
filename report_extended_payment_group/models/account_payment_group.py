from odoo import models


class AccountPaymentGroup(models.Model):
    _inherit = 'account.payment.group'

    def payment_print(self):
        self.ensure_one()
        self.sent = True

        # if we print caming from other model then active id and active model
        # is wrong and it raise an error with custom filename
        self = self.with_context(
            active_model=self._name, active_id=self.id, active_ids=self.ids)

        return self.env['ir.actions.report'].get_report(self).report_action(
            self)
