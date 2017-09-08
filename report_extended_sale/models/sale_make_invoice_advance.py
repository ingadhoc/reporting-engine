# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        invoice = super(SaleAdvancePaymentInv, self)._create_invoice(
            order=order, so_line=so_line, amount=amount)
        if order.company_id.internal_notes:
            invoice.internal_notes = order.internal_notes
        if order.company_id.external_notes:
            invoice.comment = order.note
        return invoice
