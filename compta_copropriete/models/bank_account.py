# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class BankAccount(models.Model):
    _name = 'syndic.compta.bank.account'

    name = fields.Char('Name')
    account_id = fields.Many2one('syndic.compta.pcmn', 'Compte comptable')
