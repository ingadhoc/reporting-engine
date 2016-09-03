# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, fields
# from openerp.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)


class PrintingPrinterUpdateWizard(models.TransientModel):
    _inherit = 'printing.printer.update.wizard'

    printer_type = fields.Selection([
        ('cups', 'CUPS'),
        ('gcp', 'Google Cloud Print')],
        required=True,
        default='gcp',
    )

    @api.multi
    def action_ok(self):
        self.ensure_one()
        if self.printer_type == 'cups':
            return super(PrintingPrinterUpdateWizard, self).action_ok()
        # update generic printers
        self.env['printing.printer'].update_gc_printers()
        # update users printers
        self.env['res.users'].search([
            ('google_cloudprint_rtoken', '!=', False)
        ]).update_user_gc_printers()
        return {
            'name': 'Printers',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'printing.printer',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
