from odoo import http
from odoo.http import request
from odoo.addons.syndic_tools.syndic_tools import SyndicTools


import json

class ReportController(http.Controller):
    @http.route([
        '/multi_report/<actions>/<docids>',
    ], type='http', auth='user', website=True)
    def multi_report_routes(self, actions, docids=None, **data):
        if docids:
            docids = [int(i) for i in docids.split(',')]
        if actions:
            actions = [int(i) for i in actions.split(',')]
        pdf = []
        pdf_len = 0
        for action in request.env['ir.actions.report'].browse(actions):
            pdf_data = action.render_qweb_pdf(docids, data=data)[0]
            pdf.append(pdf_data)
            pdf_len += len(pdf_data)
        
        pdf_merge = SyndicTools().merge_pdf(pdf)
        
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        return request.make_response(pdf_merge, headers=pdfhttpheaders)