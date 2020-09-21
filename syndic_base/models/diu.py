from odoo import models, fields, api, exceptions


class DIU(models.Model):
    _name = 'syndic.building.diu'
    _description = 'building.diu'

    supplier_id = fields.Many2one(
        'res.partner',
        'Fournisseur',
        required=True,
        domain=[('supplier', '=', True)]
    )
    diu_date = fields.Date('Date')
    diu_concerne = fields.Char('Type de travaux')
    diu_id = fields.Many2one('syndic.building', string='DIU')
