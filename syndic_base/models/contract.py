# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Bank(models.Model):
    _name = 'syndic.building.contract'
    _inherit = 'barcode.import'

    _barcode_type = 'contrat'
    _building_field = 'building_id'

    name = fields.Char('Contrat', required=True)
    description = fields.Char('Description', required=True)
    building_id = fields.Many2one('syndic.building', 'Immeuble', required=True)
    supplier_id = fields.Many2one('res.partner', 'Fournisseur', domain=[('supplier', '=', True)], required=True)
