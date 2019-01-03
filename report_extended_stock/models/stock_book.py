##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class StockBook(models.Model):
    _inherit = 'stock.book'

    report_partner_id = fields.Many2one(
        'res.partner',
    )
