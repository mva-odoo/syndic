# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from openerp.addons.syndic_tools.syndic_tools import SyndicTools


class SyndicFacturation(models.Model):
    _name = 'syndic.facturation'
    _inherit = 'pdf.viewer'
    _report_name = 'syndic_facturation.facture'
    _order = 'id desc'

    name = fields.Char('Facture', readonly=True)
    immeuble_id = fields.Many2one('syndic.building', string='Immeuble', required=True)
    line_ids = fields.One2many('syndic.facturation.line', 'facture_id', string='Lignes de facture')
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    date = fields.Date('Date de création', default=lambda *a: fields.date.today())
    date_fr = fields.Char(string='Date', compute='_compute_date', store=True)
    object = fields.Char('Objet')

    @api.one
    @api.depends('date')
    def _compute_date(self):
        if self.date:
            self.date_fr = SyndicTools().french_date(self.date)

    @api.model
    def create(self, vals):
        new_id = super(SyndicFacturation, self).create(vals)
        new_id.name = 'Facture %i' % new_id
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
    type_id = fields.Many2one('syndic.facturation.type', string='Type de frais', required=True)
    facture_id = fields.Many2one('syndic.facturation', string='facture')
    nombre = fields.Float('Nombre')
    prix = fields.Float('Prix de la prestation', required=True)
    prix_tot = fields.Float('Prix de la prestation', compute='_compute_tot_hours', store=True)
    qty_id = fields.Many2one('syndic.qty.type', 'Unité')

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
    prix = fields.Float('Prix de la prestation')


class SyndicqtyType(models.Model):
    _name = 'syndic.qty.type'

    name = fields.Char('Quantité', required=True)
