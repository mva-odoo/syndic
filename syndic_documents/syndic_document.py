# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
import random


class Document(models.Model):
    _name = 'syndic.documents'
    _rec_name = 'nom_document'

    nom_document = fields.Char('nom du document', required=True)
    create_date = fields.Datetime('Date de création')
    document = fields.Binary('document', required=True)
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')
    datas_fname = fields.Char("File Name")
    proprio_ids = fields.Many2many('syndic.owner', string='Propriétaires')
    building_id = fields.Many2one('syndic.building', 'Immeubles')
    type_id = fields.Many2one('syndic.type.document', 'Type de document')
    user_ids = fields.Many2many('res.users', store=True, string='Users')

    @api.onchange('proprio_ids')
    def onchange_proprio(self):
        user_ids = []
        for proprio_id in self.proprio_ids:
            if proprio_id.user_id:
                user_ids.append(proprio_id.user_id.id)
            else:
                # TODO: remove and replace with a script
                search_user = self.env['res.users'].search([('login', '=', proprio_id.login)])
                if search_user:
                    user_ids.append(search_user[0])
                    proprio_id.user_id = search_user[0]
                else:
                    login = proprio_id.name+str(int(random.random()*100))
                    password = proprio_id.name+str(int(random.random()*100000))

                    dict_users = {
                        'login': login,
                        'password': password,
                        'name': proprio_id.name,
                    }

                    group_ids = self.env['res.groups'].search(['|', ('name', 'ilike', 'Syndic/Client'),
                                                               ('name', 'ilike', 'Portal')])
                    groups = []
                    for group_id in group_ids:
                        groups.append((4, group_id))
                    dict_users['groups_id'] = groups
                    user_create_id = self.env['res.users'].sudo().create(dict_users)
                    proprio_id.write({'password': password, 'login': login, 'user_id': user_create_id})
                    user_ids.append(user_create_id)
        self.user_ids = user_ids


class Proprio(models.Model):
    _inherit = 'syndic.owner'

    document_ids = fields.Many2many('syndic.documents', string='documents')


class TypeDocument(models.Model):
    _name = 'syndic.type.document'

    name = fields.Char('name')
