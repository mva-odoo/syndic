# -*- coding: utf-8 -*-
from odoo import http


class Academy(http.Controller):
    @http.route('/sign/ag/<answer>/', auth='public', type='json')
    def index(self, answer, **kw):
        input_user = http.request.env['survey.user_input'].sudo().search([('id', '=', int(answer))])
        input_user.sign_bin = kw.get('signature')
        input_user.sign_name = kw.get('name')
        return ""
