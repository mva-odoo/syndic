# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
import random


class Document(models.Model):
    _name = 'syndic.documents'
    _description = 'syndic.documents'
    _rec_name = 'nom_document'

    nom_document = fields.Char('nom du document', required=True)
    create_date = fields.Datetime(u'Date de création')
    document = fields.Binary('document', required=True)
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')
    datas_fname = fields.Char("File Name")
    proprio_ids = fields.Many2many('res.partner', 'syndic_documents_owner_rel', string=u'Propriétaires')
    building_id = fields.Many2one('syndic.building', 'Immeubles')
    type_id = fields.Many2one('syndic.type.document', 'Type de document')
    all_document = fields.Boolean('Pour tout le batiment')


class Proprio(models.Model):
    _inherit = 'res.partner'

    document_ids = fields.Many2many('syndic.documents', string='documents')


class TypeDocument(models.Model):
    _name = 'syndic.type.document'
    _description = 'syndic.type.document'

    name = fields.Char('name', required=True)
