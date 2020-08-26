from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_private = fields.Boolean('Gestion Privative', compute="_get_private", store=True)

    @api.depends('lot_ids.is_private')
    def _get_private(self):
        for rec in self:
            rec.is_private = True if any(rec.mapped('lot_ids.is_private')) else False
