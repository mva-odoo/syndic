# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Pcmn(models.Model):
    _name = 'syndic.compta.pcmn'
    _rec_name = 'code'

    name = fields.Char('Nom du compte', required=True)
    code = fields.Char('Code du compte', required=True)
    parent_id = fields.Many2one('syndic.pcmn', 'Compte parent')
    main_compte = fields.Boolean('Compte Général')
    type_account = fields.Selection([('roulement', 'Roulement'), ('reserve', 'Reserve')])
    child_ids = fields.One2many('syndic.compta.pcmn', 'parent_id', string="Compte(s) enfant(s)")
    description = fields.Text('Description')
    immeuble_id = fields.Many2one('syndic.building', 'immeuble')

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