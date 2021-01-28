# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class Buiilding(models.Model):
    _inherit = 'syndic.building'

    document_ids = fields.One2many('syndic.documents', 'building_id', string='documents')

    def get_document(self):
        self.ensure_one()
        action = self.env.ref('syndic_documents.action_syndic_document').sudo().read()[0]
        action['domain'] = [('immeuble_id', '=', self.id)]
        action['context'] = {}
        return action
