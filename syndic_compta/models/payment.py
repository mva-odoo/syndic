# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions

class SyndicPayment(models.Model):
    _name = 'syndic.payment'

    amount = fields.Integer('Montant payé')
    facture_id = fields.Many2one('syndic.facturation', 'Facture associé Facture')
    communication = fields.Char('Communication')
