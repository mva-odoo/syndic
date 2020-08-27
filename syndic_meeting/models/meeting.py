# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.addons.syndic_tools.syndic_tools import SyndicTools


class LetterReunion(models.Model):
    _name = 'letter.reunion'
    _description = 'letter.reunion'
    _order = 'create_date desc'
            
    name = fields.Char(u'Réunion', required=True)
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble', required=True)
    descriptif = fields.Html('Descriptif')
    point_ids = fields.One2many('reunion.point', 'reunion_id', 'Points')
    create_date = fields.Datetime(u'Date de création', readonly=True)
    write_date = fields.Datetime('Write Date', readonly=True)
    type_id = fields.Many2one('reunion.type', 'Type', required=True)
    date = fields.Date(u'Date de la réunion', default=lambda *a: fields.date.today(), copy=False)
    date_fr = fields.Char(string='Date', compute='_compute_date', store=True)
    survey_id = fields.Many2one('survey.survey', 'Questionaire')

    @api.depends('date')
    def _compute_date(self):
        for reunion in self:
            if reunion.date:
                reunion.date_fr = SyndicTools().french_date(reunion.date)


class ReunionType(models.Model):
    _name = 'reunion.type'
    _description = 'reunion.type'

    name = fields.Char('Type', required=True)


class ReunionPoint(models.Model):
    _name = 'reunion.point'
    _description = 'reunion.point'
    _order = 'sequence'

    name = fields.Char('Point', required=True)
    sequence = fields.Integer(u'Numéros de point')
    reunion_id = fields.Many2one('letter.reunion', 'Reunion')
    descriptif = fields.Html('Description')
