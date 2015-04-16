# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
import datetime
import locale

class letter_avis(models.Model):
    _name = 'letter.avis'
    
    @api.one
    @api.depends('date')
    def _compute_date(self):
        if self.date:
            now = datetime.datetime.strptime(self.date, '%Y-%m-%d')
            try:
                locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')
            except Exception:
                locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')
            date_fr = now.strftime("%A %d %B %Y")
            self.date_fr = date_fr

    name = fields.Char('Nom de l’avis', required=True)
    text = fields.Html('Texte')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')
    create_date = fields.Datetime('Date de création', readonly=True)
    write_date = fields.Datetime('Write Date', readonly=True)
    date = fields.Date('Date de création', default=lambda *a: fields.date.today())
    date_fr = fields.Char(string='Date', compute='_compute_date', store=True)
    type_id = fields.Many2one('type.avis', "Type d'avis", required=True)
    avis_model_id = fields.Many2one("letter.avis.model", "Modele d'avis")

    _order = 'create_date desc'

    @api.one
    def copy(self, default=None):
        default['date'] = fields.date.today()
        return super(letter_avis, self).copy(default)

    @api.onchange('avis_model_id')
    def onchange_letter_avis_model(self):
        self.text = self.avis_model_id.text


class type_avis(models.Model):
    _name = 'type.avis'
    name = fields.Char('Type', required=True)


class letter_reunion(models.Model):
    _name = 'letter.reunion'
    
    @api.one
    @api.depends('date')
    def _compute_date(self):
        if self.date:
            now = datetime.datetime.strptime(self.date, '%Y-%m-%d')
            try:
                locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')
            except Exception:
                locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')
            date_fr = now.strftime("%A %d %B %Y")
            self.date_fr = date_fr
            
    name = fields.Char('Réunion', required=True)
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble', required=True)
    descriptif = fields.Html('Descriptif')
    point_ids = fields.One2many('reunion.point', 'reunion_id', 'Points')
    create_date = fields.Datetime('Date de création', readonly=True)
    write_date = fields.Datetime('Write Date', readonly=True)
    type_id = fields.Many2one('reunion.type', 'Type', required=True)
    date = fields.Date('Date de création', default=lambda *a: fields.date.today())
    date_fr = fields.Char(string='Date', compute='_compute_date', store=True)

    _order = 'create_date desc'

    @api.onchange('date')
    def onchange_date(self):
        if self.date:
            now = datetime.datetime.strptime(self.date, '%Y-%m-%d')
            try:
                locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')
            except Exception:
                locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')
            date_fr = now.strftime("%A %d %B %Y")
            self.date_fr = date_fr

    @api.one
    def copy(self, default=None):
        default['date'] = fields.date.today()
        return super(letter_reunion, self).copy(default)


class reunion_type(models.Model):
    _name = 'reunion.type'
    name = fields.Char('Type')


class reunion_point(models.Model):
    _name = 'reunion.point'
    name = fields.Char('Point')
    sequence = fields.Integer('Numéros de point')
    reunion_id = fields.Many2one('letter.reunion', 'Reunion')
    descriptif = fields.Html('Point')

    _order = 'sequence asc'
