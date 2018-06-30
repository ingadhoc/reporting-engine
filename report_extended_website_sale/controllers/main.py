# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request


class website_sale(http.Controller):

    @http.route(['/shop/print'], type='http', auth="public", website=True)
    def print_saleorder(self):
        cr, uid, context = request.cr, SUPERUSER_ID, request.context
        sale_order_id = request.session.get('sale_last_order_id')
        sale_order = request.registry['sale.order'].browse(
            cr, uid, sale_order_id)
        if sale_order_id:
            pdf = request.registry['report'].get_pdf(
                cr, uid, [sale_order_id],
                sale_order.get_report_name(), data=None, context=context)
            pdfhttpheaders = [('Content-Type', 'application/pdf'),
                              ('Content-Length', len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            return request.redirect('/shop')
