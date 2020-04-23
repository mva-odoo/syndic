# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, SUPERUSER_ID


class Users(models.Model):
    _inherit = 'res.users'

    server_mail_id = fields.Many2one('ir.mail_server', 'Serveur Mail Sortant')

    @api.model
    def create(self, vals):
        return super(Users, self.with_context(normal_create=True)).create(vals)
