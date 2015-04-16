from openerp import http

class Academy(http.Controller):
    @http.route('/documents/', auth='user', website=True)
    def index(self, **kwargs):
        types = []
        immeubles = []
        domain = []

        docs = http.request.env['syndic.documents'].search(domain)

        for doc in docs:
            if doc.type_id:
                types.append(doc.type_id)
            elif doc.immeuble_id:
                immeubles.append(doc.immeuble_id)
        if kwargs:
            if int(kwargs.get('immeubles')):
                domain.append(('immeuble_id', '=', int(kwargs.get('immeubles'))))
            if int(kwargs.get('types')):
                domain.append(('type_id', '=', int(kwargs.get('types'))))

        docs = http.request.env['syndic.documents'].search(domain)

        return http.request.render('website_sgimmo.index', {'documents': docs, 'types': types, 'immeubles': immeubles})