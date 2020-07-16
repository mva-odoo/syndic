# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.addons.syndic_tools.syndic_tools import SyndicTools


class FacturationSyndic(models.Model):
    _name = 'syndic.facturation.syndic'
    _description = 'syndic.facturation.syndic'
    _order = 'id desc'

    sgimmo_lign_ids = fields.One2many('syndic.facturation.syndic.ligne', 'facture_syndic_id', 'Lignes', copy=True)
    year_id = fields.Many2one('syndic.facturation.syndic.year', u'Années', required=True)
    facture_tot = fields.Float('Total', compute='_compute_total_syndic', readonly=True)
    num_immeuble = fields.Char('Numeros Client')
    num_facture = fields.Char('Numeros Facture', readonly=True)
    immeuble_id = fields.Many2one('syndic.building', string='Immeuble')
    date = fields.Date(u'Date de création', default=lambda *a: fields.date.today(), copy=False)
    date_fr = fields.Char(string='Date', compute='_compute_date', store=True)
    object = fields.Char('Objet')
    name = fields.Char('Facture', readonly=True)
    fournisseur_id = fields.Many2one('res.partner', 'Fournisseur')

    @api.depends('date')
    def _compute_date(self):
        for facture in self:
            if facture.date:
                facture.date_fr = SyndicTools().french_date(self.date)

    @api.model
    def create(self, vals):
        seq_code = 'sgimmo - %s' % self.env['syndic.facturation.syndic.year'].browse(vals.get('year_id')).name
        vals['num_facture'] = self.env['ir.sequence'].next_by_code(seq_code)
        return super(FacturationSyndic, self).create(vals)

    @api.depends('sgimmo_lign_ids')
    def _compute_total_syndic(self):
        for facture in self:
            facture.facture_tot = sum(facture.sgimmo_lign_ids.mapped('prix_tot'))

    @api.onchange('immeuble_id')
    def onchange_immeuble(self):
        self.num_immeuble = "CL%04d" % self.immeuble_id.num_building


class FacturationSyndicLigne(models.Model):
    _name = 'syndic.facturation.syndic.ligne'
    _description = 'syndic.facturation.syndic.ligne'

    ref = fields.Char(u'Référence')
    description = fields.Selection([('honoraire', 'HONORAIRE'),
                                    ('administration', 'ADMINISTRATION'),
                                    ('suivi', 'SUIVI SYNDIC')], 'Description', required=False)

    type_id = fields.Many2one('syndic.facturation.syndic.ligne.type', 'Type', required=True)
    qty = fields.Float(u'Quantité', required=True)
    prix = fields.Float('Prix', required=True)
    prix_tot = fields.Float('Prix tot', compute='_compute_tot_hours', readonly=True)
    facture_syndic_id = fields.Many2one('syndic.facturation.syndic', 'Facture Syndic')

    @api.depends('qty', 'prix')
    def _compute_tot_hours(self):
        for ligne in self:
            ligne.prix_tot = ligne.prix*ligne.qty


class FacturationSyndicYear(models.Model):
    _name = 'syndic.facturation.syndic.year'
    _description = 'syndic.facturation.syndic.year'

    name = fields.Char(u'Année', required=True)
    facture_ids = fields.One2many('syndic.facturation.syndic', 'year_id', 'Facture')
    sequence_id = fields.Many2one('ir.sequence', 'Sequence')

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].sudo().create({
            'name': "sgimmo: %s" % vals['name'],
            'implementation': 'no_gap',
            'padding': 4,
            'number_increment': 1,
            'code': 'sgimmo - %s' % vals['name'],
            'prefix': 'FC',
        })
        vals['sequence_id'] = sequence.id
        return super(FacturationSyndicYear, self).create(vals)


class SyndicFacturationLineType(models.Model):
    _name = 'syndic.facturation.syndic.ligne.type'
    _description = 'syndic.facturation.syndic.ligne.type'

    name = fields.Char('Nom', required=True)
    description = fields.Char('Description')
