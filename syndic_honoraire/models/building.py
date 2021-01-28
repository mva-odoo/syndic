# -*- coding: utf-8 -*-

from odoo import api, fields, models

from datetime import date


class Building(models.Model):
    _inherit = 'syndic.building'

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.ref('base.EUR'))
    # TODO: clean
    honoraire = fields.Monetary('Honoraire', groups='syndic_base.syndic_manager')
    frais_admin = fields.Monetary('Frais Administratif', groups='syndic_base.syndic_manager')

    honoraire_ids = fields.One2many(
        'syndic.honoraire',
        'building_id',
        'Honoraires et frais administration',
        groups='syndic_base.syndic_manager'
    )

    count_invoice = fields.Integer('N° de factures', compute='_get_count_invoice')
    is_merge = fields.Boolean('Fusionner les frais administratifs avec les honoraires', default=True)

    def get_invoice(self):
        self.ensure_one()
        action = self.env.ref('account.action_move_out_invoice_type').sudo().read()[0]
        action['domain'] = [
            ('partner_id', '=', self.partner_id.id)
        ]
        return action

    def _get_count_invoice(self):
        for record in self:
            record.count_invoice = self.sudo().env['account.move'].search_count([
                ('partner_id', '=', self.partner_id.id)
            ])

    @api.model
    def _get_first_year(self):
        self.env['syndic.honoraire.year'].create({'name': date.today().year})
