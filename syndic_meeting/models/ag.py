from odoo import models, fields, api, exceptions, _


class SyndicAG(models.Model):
    _name = 'syndic.ag'
    _description = 'syndic.ag'
    _rec_name = 'building_id'

    building_id = fields.Many2one('syndic.building', 'Immeuble', required=True)
    date = fields.Datetime("Date de l'AG", required=True)
    where = fields.Char("Lieu de l'AG", required=True)
    type_ag = fields.Selection([
        ('extra', 'extra-ordinaire'),
        ('statutaire', 'statutaire')], 'Type')
    send_ag = fields.Boolean('Envoyé?')
    presence_ids = fields.One2many(
        'syndic.ag.presence',
        'ag_id',
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

    def go_survey(self):
        self.ensure_one()
        if not self.survey_id:
            self.survey_id = self.env['survey.survey'].create({
                'title': 'AG - %s du %s' % (self.building_id.name, self.date)
            })

        return {
                'name': _('Ordre du jour'),
                'view_mode': 'form',
                'res_model': 'survey.survey',
                'view_id': self.env.ref('survey.survey_form').id,
                'type': 'ir.actions.act_window',
                'res_id': self.survey_id.id,
                'context': self._context,
        }


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
    ag_id = fields.Many2one('syndic.ag', 'AG')

    @api.depends('lot_ids')
    def _get_quotities(self):
        for rec in self:
            rec.quotities = sum(rec.lot_ids.mapped('quotities'))
