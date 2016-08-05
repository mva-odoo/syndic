# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Product(models.Model):
    _name = 'syndic.compta.product'

    name = fields.Char('Nom')
    amount = fields.Float('Montant')
    account_id = fields.Many2one('syndic.compta.pcmn', 'Compte')
