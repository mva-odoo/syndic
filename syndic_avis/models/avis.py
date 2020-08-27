# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.addons.syndic_tools.syndic_tools import SyndicTools


class LetterAvis(models.Model):
    _name = 'letter.avis'
    _description = 'letter.avis'
    _order = 'create_date desc'

    name = fields.Char(u'Nom de l’avis', required=True)
    text = fields.Html('Texte')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')
    create_date = fields.Datetime(u'Date de création', readonly=True)
    write_date = fields.Datetime('Write Date', readonly=True)
    date = fields.Date(u'Date de l\'avis', default=lambda *a: fields.date.today(), copy=False)
    date_fr = fields.Char(string='Date', compute='_compute_date', store=True)
    type_id = fields.Many2one('type.avis', "Type d'avis", required=True)
    avis_model_id = fields.Many2one("letter.avis.model", "Modele d'avis")

    @api.depends('date')
    def _compute_date(self):
        for avis in self:
            if avis.date:
                avis.date_fr = SyndicTools().french_date(self.date)

    @api.onchange('avis_model_id')
    def onchange_letter_avis_model(self):
        self.text = self.avis_model_id.text


class TypeAvis(models.Model):
    _name = 'type.avis'
    _description = 'type.avis'

    name = fields.Char('Type', required=True)


class LetterModelAvis(models.Model):
    _name = 'letter.avis.model'
    _description = 'letter.avis.model'

    name = fields.Char(u'Nom du modèle', required=True)
    text = fields.Html('Avis')
