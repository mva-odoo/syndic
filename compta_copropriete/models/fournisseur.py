# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Fournisseur(models.Model):
    _inherit = 'syndic.supplier'

    account_id = fields.Many2one('syndic.compta.pcmn', 'Compte Fournisseur')
