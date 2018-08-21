from odoo.addons.account.controllers.portal import PortalAccount
from odoo.exceptions import AccessError
from odoo.addons.report_aeroo.controllers.main import ReportController
from odoo.http import route, request, content_disposition


class PortalAccount(PortalAccount):

    @route()
    def portal_my_invoice_report(self, invoice_id, access_token=None, **kw):
        try:
            invoice_sudo = self._invoice_check_access(invoice_id, access_token)
        except AccessError:
            return request.redirect('/my')
        report = invoice_sudo.get_report()
        # print aeroo report as sudo, since it require access to taxes, payment
        # term, ... and portal does not have those access rights.
        if report.report_type == 'aeroo':
            rset = report.render_aeroo([invoice_id], data={})
            mimetype = ReportController.MIMETYPES.get(
                rset[1], 'application/octet-stream')
            httpheaders = [
                ('Content-Disposition', content_disposition(rset[2])),
                ('Content-Type', mimetype),
                ('Content-Length', len(rset[0]))
            ]
            return request.make_response(rset[0], headers=httpheaders)
        return super(PortalAccount, self).portal_my_invoice_report(
            invoice_id, access_token=access_token, **kw)
