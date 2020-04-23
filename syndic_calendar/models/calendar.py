# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class CreateLetter(models.Model):
    _inherit = 'calendar.event'

    building_id = fields.Many2one('syndic.building', string='Immeuble')
    attendee_string = fields.Char('Participants', compute='compute_participant')
    is_ag = fields.Boolean('AG')

    def compute_participant(self):
        for rec in self:
            rec.attendee_string = ','.join(rec.attendee_ids.mapped('name'))
