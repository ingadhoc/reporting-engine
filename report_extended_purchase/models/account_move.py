
from odoo import api, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('purchase_id')
    def purchase_order_change(self):
        """
        We need to use replacing and calling super function because, super func
        delete purchase_id link
        """
        if not self.purchase_id:
            return {}
        comment = self.purchase_id.notes
        internal_notes = self.purchase_id.internal_notes
        if self.comment:
            comment = '%s\n%s' % (self.comment, comment)
        if self.internal_notes:
            comment = '%s\n%s' % (self.internal_notes, internal_notes)
        self.comment = comment
        self.internal_notes = internal_notes
        return super().purchase_order_change()
