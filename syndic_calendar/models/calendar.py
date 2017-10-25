# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class CreateLetter(models.Model):
    _name = 'syndic.calendar'

    name = fields.Char('Nom du rendez-vous', required=True)
    start_date = fields.Datetime('Date de debut')
    end_date = fields.Datetime('Date de fin')
    where = fields.Char('Lieu')
    description = fields.Text('Description')
    owner_id = fields.Many2one('res.users', string=u'Responsable de l\'évenement', default=lambda self: self._uid)
    building_id = fields.Many2one('syndic.building', string='Immeuble')
    attendee_ids = fields.Many2many('res.users', string="Participants")
    attendee_string = fields.Char('Participants', compute='compute_participant')

    @api.one
    def compute_participant(self):
        participant = ''
        for attendee_id in self.attendee_ids:
            participant += '%s ' % attendee_id.name
        self.attendee_string = participant
