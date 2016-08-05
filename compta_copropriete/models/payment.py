# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Payment(models.Model):
    _name = 'syndic.compta.payment'

    due_amount = fields.Float('Montant du')
    paid_amount = fields.Float('Montant payé')
    facture_id = fields.Many2one('syndic.compta.facture', 'Facture')
    payment_ligne_ids = fields.One2many('syndic.compta.payment.ligne', 'payment_id', 'Payement Effectué')
    communication = fields.Char('Communication')


class PaymentLigne(models.Model):
    _name = 'syndic.compta.payment.ligne'

    due_amount = fields.Float('Montant du')
    payment_id = fields.Many2one('syndic.compta.payment', 'Payement')
