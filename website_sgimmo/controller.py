from odoo import http
import odoo
from odoo.http import request


class WebsiteDocument(http.Controller):
    @http.route('/documents/', auth='user', website=True)
    def index(self, **kwargs):
        domain = []
        if kwargs:
            if int(kwargs.get('immeubles')):
                domain.append(('immeuble_id', '=', int(kwargs.get('immeubles'))))

            if int(kwargs.get('types')):
                domain.append(('type_id', '=', int(kwargs.get('types'))))

            if kwargs.get('fname'):
                domain.append(('nom_document', 'ilike', kwargs.get('fname')))

        building_ids = http.request.env['syndic.building'].search([])
        doc_types = http.request.env['syndic.type.document'].search([])

        docs = http.request.env['syndic.documents'].search(domain)

        return http.request.render('website_sgimmo.index', {
            'documents': docs,
            'types': doc_types,
            'immeubles': building_ids
        })
