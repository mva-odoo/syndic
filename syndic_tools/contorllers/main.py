from odoo import http
from odoo.http import request
from odoo.addons.syndic_tools.syndic_tools import SyndicTools

import base64


class ReportController(http.Controller):
    @http.route([
        '/multi_pdf_downloads/<docids>',
    ], type='http', auth='user', website=True)
    def get_pdf(self, docids=None):
        # TODO: move this in sogis else it has a problem of depends
        pdf_merge = False
        if docids:
            docids = [int(i) for i in docids.split(',')]
            pdf = []
            pdf_len = 0
            for invoice in request.env['sogis.invoice'].browse(docids).filtered(lambda s:s.watermark_pdf):
                invoice.is_print = True
                pdf_data = base64.b64decode(invoice.watermark_pdf)
                pdf.append(pdf_data)
                pdf_len += len(pdf_data)

                pdf_merge = SyndicTools().merge_pdf(pdf)
            if pdf_merge:
                pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
                return request.make_response(pdf_merge, headers=pdfhttpheaders)