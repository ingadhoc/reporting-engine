##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class res_company(models.Model):
    _inherit = 'res.company'

    # TODO this parameters should be global and not per company
    internal_notes = fields.Boolean(
        'Move Internal Notes',
        default=True
    )
    external_notes = fields.Boolean(
        'Move External Notes',
        default=True
    )
