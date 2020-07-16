# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import date


class BonCommande(models.Model):
    _name = 'bon.commande'
    _inherit = ['barcode.import']
    _description = 'bon.commande'
    _order = 'date_demande desc'

    _barcode_type = 'bdc'

    name = fields.Char('Type', required=True)
    immeuble_id = fields.Many2one('syndic.building', string='Nom immeuble', required=True)
    fournisseur_id = fields.Many2one('res.partner', string='Nom du fournisseur', required=True)
    date_demande = fields.Date('Date demande')
    cloture = fields.Boolean('Cloture')
    date_cloture = fields.Date('Date cloture')

    @api.onchange('cloture')
    def onchange_cloture(self):
        self.date_cloture = date.today().strftime('%Y-%m-%d') if self.cloture else False
