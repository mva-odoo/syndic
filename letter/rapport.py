# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class RapportPoint(models.Model):
    _name = 'rapport.point'

    name = fields.Char('Titre')
    descriptif = fields.Html('Descriptif')
    num = fields.Integer('Numeros')
    rapport_ag_id = fields.Many2one('rapport.ag', 'Rapport AG')


class RapportAG(models.Model):
    _name = 'rapport.ag'

    name = fields.Char('Rapport')
    rapport_point_ids = fields.One2many('rapport.point', 'rapport_ag_id', 'Rapport AG')
