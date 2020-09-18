from odoo import api, fields, models


class Quotity(models.Model):
    _name = 'syndic.building.quotities'
    _description = 'Quotities'

    lot_id = fields.Many2one('syndic.lot', 'Lot')
    quotity_type_id = fields.Many2one('syndic.building.quotities.type', 'test')
    quotities = fields.Float('Quotitées')


class QuotityType(models.Model):
    _name = 'syndic.building.quotities.type'
    _description = 'Quotities'

    name = fields.Char(string='Name')
    building_ids = fields.Many2many('syndic.building', string="Immeubles")
