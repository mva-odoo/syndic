# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from openerp.addons.syndic_tools.syndic_tools import SyndicTools


class FacturationSyndic(models.Model):
    _name = 'syndic.facturation.syndic'
    _order = 'id desc'

    sgimmo_lign_ids = fields.One2many('syndic.facturation.syndic.ligne', 'facture_syndic_id', 'Lignes')
    year_id = fields.Many2one('syndic.facturation.syndic.year', 'Années', required=True)
    facture_tot = fields.Float('Total', compute='_compute_total_syndic', readonly=True)
    num_immeuble = fields.Char('Numeros Client')
    num_facture = fields.Char('Numeros Facture', readonly=True)
    immeuble_id = fields.Many2one('syndic.building', string='Immeuble', required=True)
    date = fields.Date('Date de création', default=lambda *a: fields.date.today())
    date_fr = fields.Char(string='Date', compute='_compute_date', store=True)
    object = fields.Char('Objet')
    name = fields.Char('Facture', readonly=True)

    @api.multi
    def copy(self, default=None):
        lign_ids = []
        print 'facturation 1'
        for lign in self.sgimmo_lign_ids:
            cpy_lign = lign.copy()
            cpy_lign.facture_syndic_id = self.id
            lign_ids.append(cpy_lign.id)
        return super(FacturationSyndic, self).copy(default={'sgimmo_lign_ids': [(6, 0, lign_ids)]})

    @api.one
    @api.depends('date')
    def _compute_date(self):
        if self.date:
            self.date_fr = SyndicTools().french_date(self.date)

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
    last_number = fields.Integer('Dernier Numeros', default='0')
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
