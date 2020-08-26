from odoo import api, fields, models


class Lot(models.Model):
    _inherit = 'syndic.lot'

    is_private = fields.Boolean('Gestion Privative')
    supplier_ids = fields.Many2many('res.partner', string='Fournisseurs')

    def remove_private_gestion(self):
        for rec in self:
            rec.is_private = False
