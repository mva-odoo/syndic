from odoo import models, fields, api, exceptions, _


class Survey(models.Model):
    _inherit = 'survey.survey'

    building_id = fields.Many2one('syndic.building', 'Immeuble', required=True)
    date = fields.Datetime("Date de l'AG", required=True)
    where = fields.Char("Lieu de l'AG", required=True)
    type_ag = fields.Selection([
        ('extra', 'extra-ordinaire'),
        ('statutaire', 'statutaire')], 'Type')
    send_ag = fields.Boolean('Envoyé?')
    presence_ids = fields.One2many(
        'syndic.ag.presence',
        'survey_id',
        'Presence',
        compute="_get_presence",
        store=True,
        readonly=False
    )
    survey_id = fields.Many2one('survey.survey', 'Questionaire')
    presence_percentage = fields.Float('Presence (%)', compute="_get_presence_presence")
    presence_quotities = fields.Float('Presence (Tot.)', compute="_get_presence_presence")

    access_mode = fields.Selection(default='token')
    is_attempts_limited = fields.Boolean(default=True)

    @api.depends('presence_ids')
    def _get_presence_presence(self):
        for rec in self:
            present = sum(rec.presence_ids.filtered(lambda s: s.presence in ['present', 'represente']).mapped('quotities'))
            total = sum(rec.presence_ids.mapped('quotities')) or 1.0

            rec.presence_quotities = present
            rec.presence_percentage = (present/total)*100

    @api.depends('building_id')
    def _get_presence(self):
        for rec in self:
            presence = self.env['syndic.ag.presence']
            rec.presence_ids = presence.browse([presence.new({
                'owner_id': owner.id,
                'lot_ids': owner.lot_ids.filtered(lambda s: s.building_id == rec.building_id),
            }).id for owner in rec.building_id.mapped('lot_ids.owner_id')])

    def action_send_survey(self):
        context = self.env.context.copy()
        context['default_partner_ids'] = [(6, 0, self.presence_ids.mapped('owner_id').ids)]
        return super(Survey, self.with_context(context)).action_send_survey()

    def action_get_result(self):
        domain = [('survey_id', '=', self.id)]
        user_input = self.env['survey.user_input_line'].search(domain)

        self.env.add_to_compute(user_input._fields['quotities_score'], user_input)
        self.env.add_to_compute(user_input._fields['percent_quotities_score'], user_input)
        self.env.add_to_compute(user_input._fields['percent_total'], user_input)

        user_input.recompute()

        survey_question = self.env['survey.question'].search([])

        self.env.add_to_compute(survey_question._fields['quotities_score'], survey_question)
        self.env.add_to_compute(survey_question._fields['percent_quotities_score'], survey_question)

        survey_question.recompute()

        return {
                'name': _('Resultat'),
                'view_mode': 'pivot,graph',
                'res_model': 'survey.user_input_line',
                'domain': domain,
                'type': 'ir.actions.act_window',
                'context': self._context,
        }


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    constr_mandatory = fields.Boolean(default=True)
    description = fields.Html('Description')
    quotity_type_id = fields.Many2one('syndic.building.quotities.type', 'Type de quotitées')
    building_id = fields.Many2one('syndic.building', 'Immeuble', related='survey_id.building_id')

    quotities_score = fields.Float(
        string='Score Quotité',
        compute='_get_score',
        store=True
    )
    percent_quotities_score = fields.Float(
        string='Score Quotité (%)',
        compute='_get_score',
        store=True
    )

    template_selection = fields.Selection([
        ('0', 'Vide'),
        ('1', '1 Propositions'),
        ('3', '3 Propositions'),
    ], default='0', string='Modèle')

    def get_result(self):
        action = self.env.ref('syndic_meeting.syndic_ag_question_action').read()[0]
        action['domain'] = [('question_id', '=', self.id)]
        return action

    @api.onchange('template_selection')
    def _onchange_template_selection(self):
        if self.template_selection == '1':
            resp = [
                (6, 0, []),
                (0, 0, {'value': "J'ai lu l'information", 'type_answer': 'ok'})
            ]
        elif self.template_selection == '3':
            resp = [
                (6, 0, []),
                (0, 0, {'value': "Je valide cette proposition", 'type_answer': 'ok'}),
                (0, 0, {'value': "Je ne valide pas cette proposition", 'type_answer': 'notok'}),
                (0, 0, {'value': "Je m'abstiens", 'type_answer': 'abstention'}),
            ]
        else:
            resp = [
                (6, 0, [])
            ]

        self.labels_ids = resp

    @api.depends('user_input_line_ids.value_suggested.type_answer')
    def _get_score(self):
        for rec in self:
            rec.quotities_score = sum(rec.user_input_line_ids.mapped('quotities_score'))
            rec.percent_quotities_score = sum(rec.user_input_line_ids.mapped('percent_quotities_score'))

    @api.model
    def default_get(self, fields):
        defaults = super(SurveyQuestion, self).default_get(fields)
        if (not fields or 'question_type' in fields):
            defaults['question_type'] = False if defaults.get('is_page') == True else 'simple_choice'
        return defaults


class SurveyLabel(models.Model):
    _inherit = 'survey.label'

    type_answer = fields.Selection([
        ('abstention', 'Abstention'),
        ('ok', 'OK'),
        ('notok', 'NOT OK'),
    ], 'Type de Reponse')


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input_line'

    quotities_score = fields.Float(
        string='Score Quotité',
        compute='_get_score',
        store=True
    )

    percent_quotities_score = fields.Float(
        string='Score Quotité (%)',
        compute='_get_score',
        store=True
    )

    percent_total = fields.Float(
        string='Total Quotité',
        compute='_get_score',
        store=True
    )

    partner_id = fields.Many2one(
        string='Propriétaire',
        related='user_input_id.partner_id',
        store=True
    )

    @api.depends(
        'value_suggested.type_answer',
        'question_id.quotity_type_id',
        'survey_id.presence_ids',
        'survey_id.presence_ids.presence',
        'survey_id.presence_ids.lot_ids'
    )

    def _get_lot(self, survey):
        return {
            presence.owner_id: {
                'lot_ids': presence.lot_ids,
                'quotities': presence.quotities
                } for presence in survey.presence_ids
            }


    def _get_score(self):
        answer = {
            'ok': 1,
            'notok': 0,
            'abstention': -1,
        }

        for rec in self:
            coeff = answer.get(rec.value_suggested.type_answer, 'Nope')

            if coeff == 'Nope':
                rec.quotities_score = 0.0
                rec.percent_quotities_score = 0.0
                rec.percent_total = 0.0

            else:
                if coeff == -1:
                    rec.percent_total = 0.0
                    rec.percent_quotities_score = 0.0
                    rec.quotities_score = 0.0

                type_id = rec.question_id.quotity_type_id

                lot_ids = rec.survey_id.presence_ids.filtered(
                    lambda s: s.owner_id == rec.user_input_id.partner_id
                ).mapped('lot_ids')

                quotities = sum(self.env['syndic.building.quotities'].search([
                    ('lot_id', 'in', lot_ids.ids),
                    ('quotity_type_id', '=', type_id.id),
                ]).mapped('quotities'))

                rec.quotities_score = quotities * coeff

                all_quotities = rec.read_group(
                    [('question_id', '=', rec.question_id.id)],
                    ['percent_total'],
                    ['question_id']
                )[0]['percent_total']

                if coeff != -1:
                    rec.percent_total = quotities
                    rec.percent_quotities_score = (rec.quotities_score / all_quotities) * 100 if all_quotities else 0.0
