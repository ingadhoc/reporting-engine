##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo.http import route, request, content_disposition
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.report_aeroo.controllers.main import ReportController


class WebsiteSaleExtended(WebsiteSale):

    @route()
    def print_saleorder(self):
        """Si el reporte es de aeroo lo renderizamos con sudo y si no
        renderizamos con sudo como hace odoo nativamente el reporte pdf.
        Para esto último no llamamos a odoo ya que el nombre del reporte podria
        """
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            sale_order = request.env['sale.order'].browse(sale_order_id)
            report = sale_order.sudo().get_report()
            if report.report_type == 'aeroo':
                rset = report.render_aeroo([sale_order_id], data={})
                mimetype = ReportController.MIMETYPES.get(
                    rset[1], 'application/octet-stream')
                httpheaders = [
                    ('Content-Disposition', content_disposition(rset[2])),
                    ('Content-Type', mimetype),
                    ('Content-Length', len(rset[0]))
                ]
                return request.make_response(rset[0], headers=httpheaders)
            else:
                pdf, _ = report.render_qweb_pdf([sale_order_id])
                pdfhttpheaders = [
                    ('Content-Type', 'application/pdf'),
                    ('Content-Length', u'%s' % len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            return request.redirect('/shop')
