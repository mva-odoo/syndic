from openerp import http
import openerp
from openerp.http import request


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


class Website(openerp.addons.web.controllers.main.Home):
    @http.route(website=True, auth="public")
    def web_login(self, *args, **kw):
        values = {}
        res = super(Website, self).web_login(*args, **kw)
        if request.httprequest.method == 'POST':
            old_uid = request.uid
            uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
            if uid is not False:
                user = request.env['res.users'].browse(uid)
                return http.redirect_with_hash(user.login_path)
            request.uid = old_uid
            values['error'] = "Wrong login/password"
            res = request.render('web.login', values)
        return res
