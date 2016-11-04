# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class BankAccount(models.Model):
    _name = 'syndic.bank.account'

    name = fields.Char('Compte', required=True)
    number = fields.Char('Numeros du compte', required=True)
    accounting_id = fields.Many2one('syndic.pcmn', 'Comptabilité')
    building_id = fields.Many2one('syndic.building', 'Immeuble')


class SyndicBuilding(models.Model):
    _inherit = 'syndic.building'

    bank_account_ids = fields.One2many('syndic.bank.account', 'building_id', 'Comptes en banque')
    exercice_ids = fields.One2many('syndic.compta.exercice', 'immeuble_id', 'Exercices')
    period_type = fields.Selection([
        ('trimestrielle', 'Trimestrielle'),
        ('annuelle', 'Annuelle'),
    ])
    @api.model
    def create(self, vals):
        self.env['ir.sequence'].sudo().create({
            'name': 'Facture - %s' % vals['name'],
            'implementation': 'no_gap',
            'padding': 8,
            'number_increment': 1,
            'code': 'Facture - %s' % vals['name'],
            'prefix': vals['name']+'/',
        })

        return super(SyndicBuilding, self).create(vals)
