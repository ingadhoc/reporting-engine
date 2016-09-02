# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api
from tempfile import mkstemp
import os
import logging
_logger = logging.getLogger(__name__)


class PrintingPrinter(models.Model):
    _inherit = "printing.printer"

    printer_type = fields.Selection([
        ('cups', 'CUPS'),
        ('gcp', 'Google Cloud Print')],
        required=True,
        default='CUPS',
    )
    # we add some help
    uri = fields.Char(help='URI in Google Print is the printer id')

    @api.model
    def update_printers_status(self):
        res = super(PrintingPrinter, self).update_printers_status()
        _logger.info('Updating Google Cloud Printers Status')
        gcprinters = self.env['google.cloudprint.config'].get_printers()
        for gcprinter in gcprinters:
            printer = self.env['printing.printer'].search(
                [('system_name', '=', gcprinter.get('name'))], limit=1)
            if printer:
                # TODO map other states
                if gcprinter.get('connectionStatus', False) == 'ONLINE':
                    status = 'available'
                else:
                    status = 'unknown'
                vals = {
                    'model': gcprinter.get('displayName', False),
                    'location': gcprinter.get('name', False),
                    'uri': gcprinter.get('id', False),
                    'status': status,
                }
                printer.write(vals)
        return res

    @api.multi
    def print_document(self, report, content, format, copies=1):
        """ Print a file

        Format could be pdf, qweb-pdf, raw, ...

        """
        self.ensure_one()
        if self.printer_type != 'gcp':
            return super(PrintingPrinter, self).print_document(
                report, content, format, copies=copies)

        fd, file_name = mkstemp()
        try:
            os.write(fd, content)
        finally:
            os.close(fd)

        options = self.print_options(report, format, copies)

        _logger.debug(
            'Sending job to Google Cloud printer %s' % (self.system_name))

        self.env['google.cloudprint.config'].submit_job(
            self.uri,
            format,
            file_name,
            options,
        )

        _logger.info("Printing job: '%s'" % (file_name))
        return True
