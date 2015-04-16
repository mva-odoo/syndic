# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
import datetime
import locale

class SyndicFacturation(models.Model):
    _name = 'syndic.facturation'

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

    name = fields.Char('Facture',readonly=True)
    immeuble_id = fields.Many2one('syndic.building', string='Immeuble', required=True)
    line_ids = fields.One2many('syndic.facturation.line', 'facture_id', string='Lignes de facture')
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    date = fields.Date('Date de création', default=lambda *a: fields.date.today())
    date_fr = fields.Char(string='Date', compute='_compute_date', store=True)
    object = fields.Char('Objet')

    @api.model
    def create(self, vals):
        new_id = super(SyndicFacturation, self).create(vals)
        new_id.name = 'Facture %i' %new_id
        return new_id

    @api.one
    @api.depends('line_ids')
    def _compute_total(self):
        total = 0.00
        for line in self.line_ids:
            total += line.prix_tot
        self.total = total

    @api.one
    def compute_price(self):
        for proprietaire_id in self.proprietaire_ids:
            proprietaire_id.prix_unitaire = self.total*(proprietaire_id.pourcentage/100)

class SyndicFacturationLine(models.Model):
    _name = 'syndic.facturation.line'
    name = fields.Char('Ligne de facturation')
    prix = fields.Float('Prix', required=True)
    type_id = fields.Many2one('syndic.facturation.type', string='Type de frais', required=True)
    facture_id = fields.Many2one('syndic.facturation', string='facture')
    nombre = fields.Integer('Nombre')
    prix = fields.Float('Prix de la prestation', required=True)
    prix_tot = fields.Float('Prix de la prestation', compute='_compute_tot_hours', store=True)
    qty_id = fields.Many2one('syndic.qty.type', 'type')

    @api.onchange('type_id')
    def _onchange_price(self):
        self.prix = self.type_id.prix

    @api.one
    @api.depends('nombre', 'prix')
    def _compute_tot_hours(self):
        self.prix_tot = self.prix*self.nombre


class SyndicFacturationType(models.Model):
    _name = 'syndic.facturation.type'
    name = fields.Char('Type de facture', required=True)
    prix = fields.Float('Prix de la prestation', required=True)

class SyndicqtyType(models.Model):
    _name = 'syndic.qty.type'
    name = fields.Char('Quantité', required=True)

