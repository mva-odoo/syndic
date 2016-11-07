# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Account(models.Model):
    _name = 'syndic.compta.account'

    account_id = fields.Many2one('syndic.compta.pcmn', 'Compte')
    debit = fields.Float('Debit')
    credit = fields.Float('Credit')
    facture_id = fields.Many2one('syndic.compta.facture', 'Facture')
