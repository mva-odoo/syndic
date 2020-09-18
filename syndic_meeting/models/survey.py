from odoo import models, fields, api, exceptions, _


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    constr_mandatory = fields.Boolean(default=True)
    description = fields.Html('Description')
    quotity_type_id = fields.Many2one('syndic.building.quotities.type', 'Type de quotitées')
    building_id = fields.Many2one('syndic.building', 'Immeuble', compute='_get_building')

    @api.depends('survey_id')
    def _get_building(self):
        for rec in self:
            rec.building_id = self.env['syndic.ag'].search([('survey_id', '=', rec.survey_id.id)], limit=1).building_id

    @api.model
    def default_get(self, fields):
        defaults = super(SurveyQuestion, self).default_get(fields)
        if (not fields or 'question_type' in fields):
            defaults['question_type'] = False if defaults.get('is_page') == True else 'simple_choice'
        return defaults
