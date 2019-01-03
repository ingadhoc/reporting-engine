##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    report_partner_id = fields.Many2one(
        'res.partner',
    )
