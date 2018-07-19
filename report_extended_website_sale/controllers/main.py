##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleExtended(WebsiteSale):

    @http.route()
    def print_saleorder(self):
        sale_order_id = request.session.get('sale_last_order_id')
        sale_order = request.env['sale.order'].browse(sale_order_id)
        if sale_order_id:
            report = request.env['ir.actions.report']._get_report_from_name(
                sale_order.get_report_name())
            pdf, _ = report.sudo().render_qweb_pdf([sale_order_id])
            pdfhttpheaders = [('Content-Type', 'application/pdf'),
                              ('Content-Length', u'%s' % len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            return request.redirect('/shop')
