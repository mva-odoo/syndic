# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions

class Users(models.Model):
    _inherit = 'res.users'
    login_path = fields.Char('Chemin de login', default='/documents', required=True)