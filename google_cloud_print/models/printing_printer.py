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

    gc_user_id = fields.Many2one(
        'res.users',
        'Google Cloud User',
    )
    printer_type = fields.Selection([
        ('cups', 'CUPS'),
        ('gcp', 'Google Cloud Print')],
        required=True,
        default='cups',
    )
    # we add some help
    uri = fields.Char(help='URI in Google Print is the printer id')

    @api.model
    def get_gc_printer(self, uri, user=None):
        domain = [
            ('uri', '=', uri),
            ('gc_user_id', '=', user and user.id or False)]
        printer = self.env['printing.printer'].search(
            domain, limit=1)
        return printer

    @api.model
    def update_gc_printers(self, user=None):
        _logger.info('Updating Google Cloud Printers')
        gcprinters = self.env['google.cloudprint.config'].get_printers(user)
        for gcprinter in gcprinters:
            printer = self.get_gc_printer(gcprinter.get('id'), user)
            # TODO remove local printers not any more on google
            if not printer and gcprinter.get('id') != '__google__docs':
                printer.create({
                    'name': "%s%s" % (
                        gcprinter['displayName'],
                        user and ' ' + user.name or ''),
                    'system_name': "%s%s" % (
                        gcprinter['name'],
                        user and ' ' + user.name or ''),
                    'model': gcprinter.get('type', False),
                    'location': gcprinter.get('proxy', False),
                    'uri': gcprinter.get('id', False),
                    'printer_type': 'gcp',
                    'status': self.get_gc_printer_status(
                        gcprinter.get('connectionStatus', False)),
                    'gc_user_id': user and user.id or False,
                    'status_message': gcprinter.get('connectionStatus', False),
                })
        return True

    @api.model
    def update_printers_status(self):
        res = super(PrintingPrinter, self).update_printers_status()
        # update generics printers
        self.update_gc_printers_status()
        # update users printers
        self.env['res.users'].search([
            ('google_cloudprint_rtoken', '!=', False)
        ]).update_user_gc_printers_status()
        return res

    @api.model
    def get_gc_printer_status(self, connectionStatus):
        if connectionStatus == 'ONLINE':
            status = 'available'
        else:
            status = 'unknown'
        return status

    @api.model
    def update_gc_printers_status(self, user=None):
        _logger.info('Updating Google Cloud Printers Status')
        gcprinters = self.env['google.cloudprint.config'].get_printers(user)
        for gcprinter in gcprinters:
            printer = self.get_gc_printer(gcprinter.get('id'), user)
            if printer:
                # TODO map other states

                vals = {
                    # 'model': gcprinter.get('displayName', False),
                    # 'location': gcprinter.get('name', False),
                    # 'uri': gcprinter.get('id', False),
                    'status': self.get_gc_printer_status(
                        gcprinter.get('connectionStatus', False)),
                }
                printer.write(vals)

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
