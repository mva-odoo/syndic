from odoo import models, fields, api, exceptions, _


class SyndicAGPresence(models.Model):
    _name = 'syndic.ag.presence'
    _description = 'syndic.ag.presence'

    lot_ids = fields.Many2many(
        'syndic.lot',
        string='Lots',
        readonly=True,
    )

    owner_id = fields.Many2one(
        'res.partner',
        string='Propriétaire',
        readonly=True,
    )
    presence = fields.Selection([
        ('present', 'Présent'),
        ('absent', 'absent'),
        ('represente', 'représenté'),
    ], required=True, default='absent')
    presence_with = fields.Char('Représenté par')
    quotities = fields.Float(compute="_get_quotities", string='Quotitées')
    survey_id = fields.Many2one('survey.survey', 'AG')
    answer_state = fields.Char('Réponse', compute="_get_answer")
    answer_id = fields.Many2one('survey.user_input', 'Réponse', compute="_get_answer")

    @api.depends('survey_id.user_input_ids')
    def _get_answer(self):
        for rec in self:
            reponse = rec.survey_id.user_input_ids.filtered(lambda s: s.partner_id == rec.owner_id)
            rec.answer_state = reponse.state if reponse else 'Non envoyé'
            rec.answer_id = reponse



    @api.depends('lot_ids')
    def _get_quotities(self):
        for rec in self:
            rec.quotities = sum(rec.lot_ids.mapped('quotities'))
