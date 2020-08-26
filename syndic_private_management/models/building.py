from odoo import api, fields, models


class Building(models.Model):
    _inherit = 'syndic.building'

    is_private = fields.Boolean('Gestion Privative', compute='_get_private', store=True, readonly=False)

    @api.depends('lot_ids.is_private')
    def _get_private(self):
        for rec in self:
            rec.is_private = True if all(rec.mapped('lot_ids.is_private')) else False
