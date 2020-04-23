from odoo import models, fields, api


class ResPartnerJob(models.Model):
    _name = 'res.partner.job'
    _description = 'res.partner.job'
    _order = 'name'

    name = fields.Char(u'Métier', requiered=True)