# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from openerp import tools


class PDFViewer(models.Model):
    _name = 'pdf.viewer'
    _report_name = 'pdf.viewer'

    @api.multi
    def report_creation(self):
        return {
            'name': 'Export ficher technique',
            'tag': 'pdf_viewer.homepage',
            'type': 'ir.actions.client',
            'context': {'report': self._report_name},
        }
