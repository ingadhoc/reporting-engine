##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    report_company_name = fields.Char(
        'Report Company Name',
        help='Company name to be printed on reports',
    )
