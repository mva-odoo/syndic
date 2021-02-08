# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class SuiviFacture(models.TransientModel):
    _name = 'syndic.facturation.creation'
    _description = 'Generer des factures honoraire'

    trimestre = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ], string='Trimestre')
    year_id = fields.Many2one('syndic.honoraire.year', u'Année')
    date = fields.Date('Date', default=lambda *a: fields.date.today())
    amount = fields.Float('Montant')
    description = fields.Char('Description')
    is_fix = fields.Boolean('Frais fix')

    def invoice_generate(self):
        self.ensure_one()
        invoices = self.env['account.move']

        active_buildings = self.env['syndic.building'].browse(self._context.get('active_ids'))
        if not self.is_fix:
            buildings = active_buildings & self.year_id.mapped('honoraire_ids.building_id')
        else:
            buildings = active_buildings

        for building in buildings:
            if not self.is_fix:
                frais = self.env['syndic.honoraire'].search([
                    ('year_id', '=', self.year_id.id),
                    ('building_id', '=', building.id)
                ], limit=1)

                frais_admin_vals = {
                    'name': 'Frais administratifs %s - %s' % (self.year_id.name, self.trimestre),
                    'price_unit': frais.frais_admin,
                    'quantity': 1,
                    # 'account_id': self.env.ref('l10n_be.1_a7010').id,

                }

                honoraire_vals = {
                    'name': 'Honoraires %s - %s' % (self.year_id.name, self.trimestre),
                    'price_unit': frais.honoraire,
                    'quantity': 1,
                    # 'account_id': self.env.ref('l10n_be.1_a7010').id,

                }

                if building.is_merge:
                    invoices |= self.env['account.move'].create({
                        'move_type': 'out_invoice',
                        'date': self.date,
                        'building_id': building.id,
                        'partner_id': building.partner_id.id,
                        'invoice_line_ids': [(0, 0, frais_admin_vals), (0, 0, honoraire_vals)]
                    })

                else:
                    invoices |= self.env['account.move'].create({
                        'move_type': 'out_invoice',
                        'date': self.date,
                        'building_id': building.id,
                        'partner_id': building.partner_id.id,
                        'invoice_line_ids': [(0, 0, frais_admin_vals)]
                    })

                    invoices |= self.env['account.move'].create({
                        'move_type': 'out_invoice',
                        'date': self.date,
                        'building_id': building.id,
                        'partner_id': building.partner_id.id,
                        'invoice_line_ids': [(0, 0, honoraire_vals)]
                    })
            else:
                invoices |= self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'date': self.date,
                    'building_id': building.id,
                    'partner_id': building.partner_id.id,
                    'invoice_line_ids': [(0, 0, {
                        'name': self.description,
                        'price_unit': self.amount,
                        'quantity': 1,
                        # 'account_id': self.env.ref('l10n_be.1_a7010').id,
                    })]
                    })
        action = self.env.ref('account.action_move_out_invoice_type').sudo().read()[0]
        action['domain'] = [('id', 'in', invoices.ids)]

        return action
