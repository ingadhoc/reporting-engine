# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    google_user = fields.Char(
    )
    google_password = fields.Char(
    )
