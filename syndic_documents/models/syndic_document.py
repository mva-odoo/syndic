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


class Proprio(models.Model):
    _inherit = 'syndic.owner'

    document_ids = fields.Many2many('syndic.documents', string='documents')


class TypeDocument(models.Model):
    _name = 'syndic.type.document'

    name = fields.Char('name', required=True)
