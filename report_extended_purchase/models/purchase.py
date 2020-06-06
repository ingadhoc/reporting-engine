##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def print_quotation(self):
        # if PO was on draft, set it on sent
        self.filtered(lambda x: x.state == 'draft').write({'state': "sent"})

        # if we print coming from other model then active id and active model
        # is wrong and it raise an error with custom filename
        self = self.with_context(
            active_model=self._name, active_id=self.id, active_ids=self.ids)

        return self.env['ir.actions.report'].get_report(self).report_action(
            self)
