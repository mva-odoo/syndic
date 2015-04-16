# -*- coding: utf-8 -*-

from openerp.addons.report.controllers.main import ReportController
from openerp.addons.web.http import route


class PdfViewerController(ReportController):
    @route(['/report/download'], type='http', auth="user")
    def report_download(self, data, token):
        response = super(PdfViewerController, self).report_download(data, token)
        response.headers.remove('Content-Disposition')
        return response
