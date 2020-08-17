# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Bank(models.Model):
    _inherit = 'res.partner.bank'

    building_id = fields.Many2one('syndic.building', 'Immeuble')

    @api.model
    def create(self, vals):
        building = self.env['syndic.building'].browse(vals.get('building_id'))
        if building:
            vals['partner_id'] = building.user_id.partner_id.id
        return super(Bank, self.sudo()).create(vals)
