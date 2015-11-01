# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions

class CreateLetter(models.Model):
    _name = 'syndic.calendar'

    name = fields.Char('Nom du rendez-vous')
    start_date = fields.Date('Date de debut')
    end_date = fields.Date('Date de fin')
    where = fields.Char('Lieu')
    allday = fields.Boolean('Toute la journée')
    description = fields.Text('Description')
