# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class ImportBarcode(models.TransientModel):
    _name = 'barecode.importation'
    _description = 'barecode.importation'

    attachment_ids = fields.Many2many('ir.attachment', string='Fichier à importer')

    def barcode_import(self):
        active_model = self.env.context.get('active_model')
        for attachment in self.attachment_ids:
            self.env[active_model].search(
                [('code', '=', attachment.name[:-4])],
                limit=1
            ).write({
                'attachment_ids': [(4, attachment.id)]
            })
