from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.report_aeroo.controllers.main import ReportController
from odoo.http import request, content_disposition
from odoo.exceptions import UserError


class PortalReportExtended(CustomerPortal):

    def _show_report(self, model, report_type, report_ref, download=False):
        """ Modificamos el metodo generico para intentar obtener report con "get_report" antes de usar el report_ref
        Ademas agregamos compatibilidad con aeroo (por ahora solo descarga archivo, deberia previsualizarlo)
        """
        if report_type not in ('html', 'pdf', 'text'):
            raise UserError("Invalid report type: %s" % report_type)

        # por ahora, comoo no podemos previsualizar reportes de aeroo, si se pide reporte html/text devolvemos reportes
        # nativos de odoo. Una vez implementado lo de abajo se puede usar siempre el get_report
        # report_sudo = model.sudo().get_report()
        report_sudo = report_type == 'pdf' and hasattr(model.sudo(), 'get_report') and model.sudo().get_report() or False

        # if we found a new report use it, if not use default report_ref
        report_ref = report_sudo and report_sudo.get_external_id()[report_sudo.id] or report_ref

        # now we fix aerro rendering
        report_sudo = request.env.ref(report_ref).sudo()
        if report_sudo.report_type != 'aeroo':
            return super()._show_report(model, report_type, report_ref, download=False)

        # TODO incorporarar que se pueda previsualizar el reporte sin descargar
        rset = report_sudo.render_aeroo([model.id], data={})
        mimetype = ReportController.MIMETYPES.get(rset[1], 'application/octet-stream')
        httpheaders = [
            ('Content-Disposition', content_disposition(rset[2])),
            ('Content-Type', mimetype),
            ('Content-Length', len(rset[0]))
        ]
        return request.make_response(rset[0], headers=httpheaders)

        # report = report_sudo.render_aeroo([model.id], data={})[0]
        # reporthttpheaders = [
        #     ('Content-Type', 'application/pdf' if report_type == 'pdf' else 'text/html'),
        #     ('Content-Length', len(report)),
        # ]
        # if report_type == 'pdf' and download:
        #     filename = "%s.pdf" % (re.sub('\W+', '-', model._get_report_base_filename()))
        #     reporthttpheaders.append(('Content-Disposition', content_disposition(filename)))
        # return request.make_response(report, headers=reporthttpheaders)
