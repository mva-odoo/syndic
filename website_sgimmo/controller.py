from openerp import http
import openerp
from openerp.http import request

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


class Website(openerp.addons.web.controllers.main.Home):
    @http.route(website=True, auth="public")
    def web_login(self, *args, **kw):
        values = {}
        res = super(Website, self).web_login(*args, **kw)
        if request.httprequest.method == 'POST':
            old_uid = request.uid
            uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
            if uid is not False:
                user = request.registry['res.users'].browse(request.cr, uid, uid, request.context)
                return http.redirect_with_hash(user.login_path)
            request.uid = old_uid
            values['error'] = "Wrong login/password"
            res = request.render('web.login', values)
        return res