##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def get_domains(self, record):
        domains = super(IrActionsReport, self).get_domains(record)
        if record._name == 'purchase.order':
            # No rules
            domains.append([])
        return domains
