# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class Lot(models.Model):
    _name = 'syndic.lot'
    _description = 'syndic.lot'
    _order = 'building_id asc,name'

    name = fields.Char('Nom du lot', required=True)
    building_id = fields.Many2one('syndic.building', 'Immeuble')
    owner_id = fields.Many2one('res.partner', 'Propriétaire')
    loaner_ids = fields.Many2many('res.partner', 'syndic_lot_loan_rel', string='Locataire')
    quotities = fields.Float(u'Quotitées')
    lot_id = fields.Many2one('syndic.lot', string='Lot')
    lot_ids = fields.One2many('syndic.lot', 'lot_id', string='sous-lots')
    type_id = fields.Many2one('syndic.type_lot', 'Type de lot')
    mutation_ids = fields.Many2many('syndic.mutation', string='Mutation')


class TypeLot(models.Model):
    _name = 'syndic.type_lot'
    _description = 'syndic.type_lot'
    _order = 'name'

    name = fields.Char('Type de lot', required=True)
