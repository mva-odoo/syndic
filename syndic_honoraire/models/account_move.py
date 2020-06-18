# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    building_id = fields.Many2one('syndic.building', 'Immeuble')
