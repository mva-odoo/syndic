# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class FacturationSyndic(models.Model):
    _name = 'syndic.facturation.syndic'
    _inherit = 'syndic.facturation'
    _order = 'id desc'

    sgimmo_lign_ids = fields.One2many('syndic.facturation.syndic.ligne', 'facture_syndic_id', 'Lignes')
    year_id = fields.Many2one('syndic.facturation.syndic.year', 'Années', required=True)
    facture_tot = fields.Float('Total', compute='_compute_total_syndic', readonly=True)
    num_immeuble = fields.Char('Numeros Client')
    num_facture = fields.Char('Numeros Facture', readonly=True)

    @api.multi
    def copy(self, default=None):
        new_lign_ids = self.sgimmo_lign_ids.copy()
        new_id = super(FacturationSyndic, self).copy(default=default)
        new_id.sgimmo_lign_ids = new_lign_ids
        return new_id

    @api.model
    def create(self, vals):
        seq_code = 'sgimmo - %s' % self.env['syndic.facturation.syndic.year'].browse(vals.get('year_id')).name
        vals['num_facture'] = self.env['ir.sequence'].next_by_code(seq_code)
        return super(FacturationSyndic, self).create(vals)

    @api.one
    @api.depends('sgimmo_lign_ids')
    def _compute_total_syndic(self):
        total = 0.00
        for line in self.sgimmo_lign_ids:
            total += line.prix_tot
        self.facture_tot = total

    @api.onchange('immeuble_id')
    def onchange_immeuble(self):
        self.num_immeuble = "CL%04d" % self.immeuble_id.num_building


class FacturationSyndicLigne(models.Model):
    _name = 'syndic.facturation.syndic.ligne'

    ref = fields.Char('Référence')
    description = fields.Selection([('honoraire', 'HONORAIRE'),
                                    ('administration', 'ADMINISTRATION'),
                                    ('suivi', 'SUIVI SYNDIC')], 'Description', required=True)
    qty = fields.Float('Quantité', required=True)
    prix = fields.Float('Prix', required=True)
    prix_tot = fields.Float('Prix tot', compute='_compute_tot_hours', readonly=True)
    facture_syndic_id = fields.Many2one('syndic.facturation.syndic', 'Facture Syndic')

    @api.one
    @api.depends('qty', 'prix')
    def _compute_tot_hours(self):
        self.prix_tot = self.prix*self.qty


class FacturationSyndicYear(models.Model):
    _name = 'syndic.facturation.syndic.year'

    name = fields.Char('Année', required=True)
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
