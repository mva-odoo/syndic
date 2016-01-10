# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class FacturationSyndic(models.Model):
    _name = 'syndic.facturation.syndic'
    _inherit = 'syndic.facturation'
    _report_name = 'sgimmo_facturation.facture'
    _order = 'id desc'

    sgimmo_lign_ids = fields.One2many('syndic.facturation.syndic.ligne', 'facture_syndic_id', 'Lignes')
    year_id = fields.Many2one('syndic.facturation.syndic.year', 'Années', required=True)
    facture_tot = fields.Float('Total', compute='_compute_total_syndic', readonly=True)
    num_immeuble = fields.Char('Numeros Client')
    num_facture = fields.Char('Numeros Client', readonly=True)

    @api.multi
    def copy(self, default=None):
        return super(FacturationSyndic, self).copy(default)

    @api.model
    def create(self, vals):
        year = self.env['syndic.facturation.syndic.year'].browse(vals.get('year_id'))

        num_facture = year.last_number+1

        vals['num_facture'] = 'FC%04d' % num_facture
        year.write({'last_number': num_facture})
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
    description = fields.Selection([('honoraire', 'HORAIRE'),
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
    last_number = fields.Integer('Dernier Numeros', default='0')
    facture_ids = fields.One2many('syndic.facturation.syndic', 'year_id', 'Facture')

