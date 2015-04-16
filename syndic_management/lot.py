# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions

class lot(models.Model):
    _name = 'syndic.lot'

    name = fields.Char('Nom du lot')
    building_id = fields.Many2one('syndic.building', 'Immeuble')
    proprio_id = fields.Many2many('syndic.owner', string='Propriétaire')
    locataire_id = fields.Many2many('syndic.loaner', string='Locataire')
    quotities = fields.Float('Quotitées')
    lot_id = fields.Many2one('syndic.lot', string='Lot')
    lot_ids = fields.One2many('syndic.lot', 'lot_id', string='Lots')#recuresivité
    type_id = fields.Many2one('syndic.type_lot', 'Type de lot')

    _order = 'building_id asc,name'

class type_lot(models.Model):
    _name = 'syndic.type_lot'
    name = fields.Char('Type de lot')
    _order = 'name'