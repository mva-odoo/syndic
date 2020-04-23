# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Bank(models.Model):
    _inherit = 'res.partner.bank'

    building_id = fields.Many2one('syndic.building', 'Immeuble')

    def create(self, values):
        building = self.env['syndic.building'].browse(values.get('building_id'))
        # if building:
            # self.env.user.company_ids |= building.company_id
            # values['company_id'] = building.company_id.id
            # values['partner_id'] = building.partner_id.id

        return super(Bank, self.sudo()).create(values)
