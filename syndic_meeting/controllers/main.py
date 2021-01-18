# -*- coding: utf-8 -*-
from odoo import http


from datetime import datetime


class Academy(http.Controller):
    @http.route('/sign/ag/<answer>/', auth='public', type='json')
    def index(self, answer, **kw):
        input_user = http.request.env['survey.user_input'].sudo().search([('id', '=', int(answer))])
        input_user.sign_bin = kw.get('signature')
        input_user.sign_name = kw.get('name')
        input_user.ip_address = http.request.httprequest.environ['REMOTE_ADDR']
        input_user.date = datetime.now()
        return ""
