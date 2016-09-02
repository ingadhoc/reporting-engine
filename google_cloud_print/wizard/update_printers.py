# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, fields
# from openerp.exceptions import Warning
from openerp.addons.google_cloud_print.google_cloud_print import *
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
        _logger.info('Updating Google Cloud Printers')
        gcprinters = self.env['google.cloudprint.config'].get_printers()
        for gcprinter in gcprinters:
            printer = self.env['printing.printer'].search(
                [('system_name', '=', gcprinter.get('name'))], limit=1)
            # TODO remove local printers not any more on google
            if not printer and gcprinter.get('id') != '__google__docs':
                printer.create({
                    'name': gcprinter['displayName'],
                    'system_name': gcprinter['name'],
                    'model': gcprinter.get('type', False),
                    'location': gcprinter.get('proxy', False),
                    'uri': gcprinter.get('id', False),
                    'printer_type': 'gcp',
                    'status': 'unknown',
                    'status_message': gcprinter.get('connectionStatus', False),
                })
        return {
            'name': 'Printers',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'printing.printer',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
