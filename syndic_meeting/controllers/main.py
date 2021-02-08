# -*- coding: utf-8 -*-
from odoo import http


from datetime import datetime
from odoo.addons.survey.controllers.main import Survey


class Academy(http.Controller):
    @http.route('/sign/ag/<answer>/', auth='public', type='json')
    def sign_json(self, answer, **kw):
        input_user = http.request.env['survey.user_input'].sudo().search([('id', '=', int(answer))])
        input_user.sign_bin = kw.get('signature')
        input_user.sign_name = kw.get('name')
        input_user.ip_address = http.request.httprequest.environ['REMOTE_ADDR']
        input_user.date = datetime.now()
        return {
            'redirect_url': '/sign/ag/thank-you/',
            'force_refresh': True,
        }

    @http.route('/sign/ag/thank-you/', auth='public', type='http')
    def sign_thankyou(self):
        return http.request.render(
            'syndic_meeting.syndic_survey_thank_you_sign',
            {}
        )


class Survey(Survey):
    def _check_validity(self, survey_token, answer_token, ensure_token=True):
        # check if the user is in the AG presence to be sure a owner can not access to an other building AG
        survey_sudo, answer_sudo = self._fetch_from_access_token(survey_token, answer_token)
        user = http.request.env['res.users'].browse(http.request._uid)
        if not user.has_group('base.group_user') and (user.partner_id not in survey_sudo.presence_ids.owner_id) and survey_sudo.building_id:
            return 'survey_auth'

        return super(Survey, self)._check_validity(survey_token, answer_token, ensure_token)

    # def survey_display_page(self, survey_token, answer_token, **post):
    #     print('----------->')
    #     return super().survey_display_page(survey_token, answer_token, **post)

    @http.route('/survey/start/<string:survey_token>', type='http', auth='public', website=True)
    def survey_start(self, survey_token, answer_token=None, email=False, **post):
        survey = http.request.env['survey.survey'].sudo().search([('access_token', '=', survey_token)], limit=1)

        present = survey.presence_ids.filtered(lambda s: s.owner_id == http.request.env.user.partner_id)
        present.write({
            'date_connexion': datetime.now()
        })

        return super().survey_start(survey_token, answer_token, email, **post)