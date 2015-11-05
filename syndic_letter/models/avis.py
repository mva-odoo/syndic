# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from openerp.addons.syndic_tools.syndic_tools import UCLTools


class LetterAvis(models.Model):
    _name = 'letter.avis'
    _order = 'create_date desc'
    _inherit = 'pdf.viewer'
    _report_name = 'syndic_letter.avis_impression'

    name = fields.Char('Nom de l’avis', required=True)
    text = fields.Html('Texte')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')
    create_date = fields.Datetime('Date de création', readonly=True)
    write_date = fields.Datetime('Write Date', readonly=True)
    date = fields.Date('Date de création', default=lambda *a: fields.date.today())
    date_fr = fields.Char(string='Date', compute='_compute_date', store=True)
    type_id = fields.Many2one('type.avis', "Type d'avis", required=True)
    avis_model_id = fields.Many2one("letter.avis.model", "Modele d'avis")

    @api.one
    @api.depends('date')
    def _compute_date(self):
        if self.date:
            self.date_fr = UCLTools().french_date(self.date)

    @api.one
    def copy(self, default=None):
        default['date'] = fields.date.today()
        return super(LetterAvis, self).copy(default)

    @api.onchange('avis_model_id')
    def onchange_letter_avis_model(self):
        self.text = self.avis_model_id.text


class TypeAvis(models.Model):
    _name = 'type.avis'

    name = fields.Char('Type', required=True)


class LetterReunion(models.Model):
    _name = 'letter.reunion'
    _order = 'create_date desc'
    _inherit = 'pdf.viewer'
    _report_name = 'syndic_letter.rapport_reunion_print'
            
    name = fields.Char('Réunion', required=True)
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble', required=True)
    descriptif = fields.Html('Descriptif')
    point_ids = fields.One2many('reunion.point', 'reunion_id', 'Points')
    create_date = fields.Datetime('Date de création', readonly=True)
    write_date = fields.Datetime('Write Date', readonly=True)
    type_id = fields.Many2one('reunion.type', 'Type', required=True)
    date = fields.Date('Date de création', default=lambda *a: fields.date.today())
    date_fr = fields.Char(string='Date', compute='_compute_date', store=True)

    @api.one
    @api.depends('date')
    def _compute_date(self):
        if self.date:
            self.date_fr = UCLTools().french_date(self.date)

    @api.onchange('date')
    def onchange_date(self):
        if self.date:
            self.date_fr = UCLTools().french_date(self.date)

    @api.one
    def copy(self, default=None):
        default['date'] = fields.date.today()
        return super(LetterReunion, self).copy(default)


class ReunionType(models.Model):
    _name = 'reunion.type'

    name = fields.Char('Type', required=True)


class ReunionPoint(models.Model):
    _name = 'reunion.point'
    _order = 'create_date desc'

    name = fields.Char('Point', required=True)
    sequence = fields.Integer('Numéros de point')
    reunion_id = fields.Many2one('letter.reunion', 'Reunion')
    descriptif = fields.Html('Point')
