# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
import datetime

class Pcmn(models.Model):
    _name = 'syndic.pcmn'
    _rec_name = 'code'
    name = fields.Char('Nom du compte', required=True)
    code = fields.Char('Code du compte', required=True)
    parent_id = fields.Many2one('syndic.pcmn', 'Compte parent')
    main_compte = fields.Boolean('Compte Général')
    type_account = fields.Selection([('roulement', 'Roulement'), ('reserve', 'Reserve')])
    child_ids = fields.One2many('syndic.pcmn', 'parent_id', string="Compte(s) enfant(s)")

    @api.multi
    def name_get(self):
        res = []
        for pcmn in self:
            name = "%s-%s" % (pcmn.code, pcmn.name)
            res += [(pcmn.id, name)]
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            args = ['|', ('name', operator, name), ('code', operator, name)] + args
        pcmn = self.search(args, limit=limit)
        return pcmn.name_get()

class Prodcut(models.Model):
    _name = 'syndic.product'
    name = fields.Char('Produit')
    detail = fields.Text('Detail')
    payable_compte_id = fields.Many2one('syndic.pcmn', 'Compte payé')
    receive_compte_id = fields.Many2one('syndic.pcmn', 'Compte Reçu')
    etablissement_fond = fields.Many2one('syndic.pcmn', 'etabblissement de fond')
    accompte_fond_id = fields.Many2one('syndic.pcmn', 'accompte de fond')
    account_product = fields.Boolean('Produit comptable')