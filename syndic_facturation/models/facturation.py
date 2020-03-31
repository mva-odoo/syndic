# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.addons.syndic_tools.syndic_tools import SyndicTools


class SuiviFacture(models.Model):
    _name = 'syndic.facturation'
    _order = 'id desc'

    name = fields.Char('Facture', readonly=True)
    immeuble_id = fields.Many2one('syndic.building', string='Immeuble', required=True)
    line_ids = fields.One2many('syndic.facturation.line', 'facture_id', string='Lignes de facture', copy=True)
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    date = fields.Date(u'Date de création', default=lambda *a: fields.date.today(), copy=False)
    date_fr = fields.Char(string='Date', compute='_compute_date', store=True)
    object = fields.Char('Objet')

    facture_type = fields.Selection([
        ('suivi_syndic', 'Suivis Syndic'),
        ('fraisadmin', 'Frais Administratifs'),
        ('honoraire', 'Honoraires'),
    ], 'Type de facture')

    facture_type2 = fields.Selection([
        ('fraisadmin', 'Frais Administratifs'),
        ('honoraire', 'Honoraires'),
    ], 'Type de facture')

    trimestre = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ], string='Trimestre')
    year = fields.Char(u"Année")

    @api.onchange('facture_type2')
    def onchange_type(self):
        self.facture_type = self.facture_type2

    @api.depends('date')
    def _compute_date(self):
        for facturation in self:
            if self.date:
                self.date_fr = SyndicTools().french_date(self.date)

    @api.model
    def create(self, vals):
        if vals.get('facture_type') == 'suivi_syndic':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                self.env.ref('syndic_facturation.sequence_facture_sgimmo').code)
        elif vals.get('facture_type') == 'honoraire':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                self.env.ref('syndic_facturation.sequence_honoraire_sgimmo').code)
        elif vals.get('facture_type') == 'fraisadmin':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                self.env.ref('syndic_facturation.sequence_fraisadmin').code)
        else:
            vals['name'] = 'Facture Non Typée'

        return super(SuiviFacture, self).create(vals)

    @api.depends('line_ids')
    def _compute_total(self):
        for facturation in self:
            facturation.total = sum(facturation.line_ids.mapped('prix_tot')) if facturation.line_ids else 0.00

    def compute_price(self):
        for facturation in self:
            for proprietaire_id in facturation.proprietaire_ids:
                proprietaire_id.prix_unitaire = facturation.total*(proprietaire_id.pourcentage/100)


class SyndicFacturationLine(models.Model):
    _name = 'syndic.facturation.line'

    name = fields.Char('Ligne de facturation')
    type_id = fields.Many2one('syndic.facturation.type', string='Type de frais')
    facture_id = fields.Many2one('syndic.facturation', string='facture')
    nombre = fields.Float('Nombre', default=1.00)
    prix = fields.Float('Prix de la prestation', required=True)
    prix_tot = fields.Float('Prix de la prestation', compute='_compute_tot_hours', store=True)
    qty_id = fields.Many2one('syndic.qty.type', u'Unité')

    @api.onchange('type_id')
    def _onchange_price(self):
        self.prix = self.type_id.prix

    @api.depends('nombre', 'prix')
    def _compute_tot_hours(self):
        for line in self:
            line.prix_tot = line.prix*line.nombre


class SyndicFacturationType(models.Model):
    _name = 'syndic.facturation.type'

    name = fields.Char('Type de facture', required=True)
    prix = fields.Float('Prix de la prestation')


class SyndicqtyType(models.Model):
    _name = 'syndic.qty.type'

    name = fields.Char(u'Quantité', required=True)
