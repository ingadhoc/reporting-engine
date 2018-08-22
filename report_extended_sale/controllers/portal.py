from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.exceptions import AccessError
from odoo.addons.report_aeroo.controllers.main import ReportController
from odoo.http import route, request, content_disposition


class CustomerPortal(CustomerPortal):

    @route()
    def portal_order_report(self, order_id, access_token=None, **kw):
        try:
            order_sudo = self._order_check_access(order_id, access_token)
        except AccessError:
            return request.redirect('/my')
        report = order_sudo.get_report()
        # print aeroo report as sudo, since it require access to taxes, payment
        # term, ... and portal does not have those access rights.
        if report.report_type == 'aeroo':
            rset = report.render_aeroo([order_id], data={})
            mimetype = ReportController.MIMETYPES.get(
                rset[1], 'application/octet-stream')
            httpheaders = [
                ('Content-Disposition', content_disposition(rset[2])),
                ('Content-Type', mimetype),
                ('Content-Length', len(rset[0]))
            ]
            return request.make_response(rset[0], headers=httpheaders)
        return super(CustomerPortal, self).portal_order_report(
            order_id, access_token=access_token, **kw)
