# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from openerp.addons.syndic_tools.syndic_tools import SyndicTools


class SuiviFacture(models.Model):
    _name = 'syndic.facturation'
    _order = 'id desc'

    name = fields.Char('Facture', readonly=True)
    immeuble_id = fields.Many2one('syndic.building', string='Immeuble', required=True)
    line_ids = fields.One2many('syndic.facturation.line', 'facture_id', string='Lignes de facture')
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    date = fields.Date('Date de création', default=lambda *a: fields.date.today())
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
    year = fields.Char("Année")

    @api.onchange('facture_type2')
    def onchange_type(self):
        self.facture_type = self.facture_type2

    @api.multi
    def copy(self, default=None):
        new_lign_ids = self.line_ids.copy()
        new_id = super(SuiviFacture, self).copy(default=default)
        new_id.line_ids = new_lign_ids
        return new_id

    @api.one
    @api.depends('date')
    def _compute_date(self):
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

    @api.one
    @api.depends('line_ids')
    def _compute_total(self):
        self.total = sum(self.line_ids.mapped('prix_tot')) if self.line_ids else 0.00

    @api.one
    def compute_price(self):
        for proprietaire_id in self.proprietaire_ids:
            proprietaire_id.prix_unitaire = self.total*(proprietaire_id.pourcentage/100)


class SyndicFacturationLine(models.Model):
    _name = 'syndic.facturation.line'

    name = fields.Char('Ligne de facturation')
    type_id = fields.Many2one('syndic.facturation.type', string='Type de frais')
    facture_id = fields.Many2one('syndic.facturation', string='facture')
    nombre = fields.Float('Nombre', default=1.00)
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
