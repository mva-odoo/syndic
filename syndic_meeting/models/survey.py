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


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    constr_mandatory = fields.Boolean(default=True)
    description = fields.Html('Description')
    quotity_type_id = fields.Many2one('syndic.building.quotities.type', 'Type de quotitées')
    building_id = fields.Many2one('syndic.building', 'Immeuble', related='survey_id.building_id')

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
