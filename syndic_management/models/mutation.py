# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Mutation(models.Model):
    _name = 'syndic.mutation'

    mutation_date = fields.Date('Date de mutation')
    old_owner_ids = fields.Many2many('syndic.owner', 'old_owner_table', string='Ancien Propriétaire', required=True)
    new_owner_ids = fields.Many2many('syndic.owner', 'new_owner_table', string='Nouveau Propriétaire', required=True)
    lot_ids = fields.Many2many('syndic.lot', string='Lot', required=True)
    state = fields.Selection([('draft', 'brouillon'), ('done', 'terminé')], 'Etat', default='draft')
    immeuble_id = fields.Many2one('syndic.building', related='lot_ids.building_id', store=True, string="Immeuble")

    @api.onchange('old_owner_ids')
    def onchange_old_owner(self):
        return {
            'domain': {'lot_ids': [('proprio_id', 'in',  self.old_owner_ids.ids)]}
        }

    @api.one
    def new_owner_lot(self, lots, new_ids):
        lots.write({'proprio_id': [(6, 0, new_ids)]})

    @api.one
    def check_last_lot(self, old_ids):
        res = False
        if not self.env['syndic.lot'].search([('proprio_id', 'in', old_ids)]):
            res = True
        return res

    @api.one
    def change_to_old_owner(self, old_ids, lots, mutation_date):
        for old_id in old_ids:
            self.env['syndic.old.owner'].create({
                'proprio_id': old_id,
                'lot_ids': [(6, 0, lots)],
                'date_close': mutation_date
            })

    @api.one
    def remove_access_users(self, old_ids):
        user_ids = self.env['res.users'].search([('proprio_id', 'in', old_ids)])
        user_ids.unlink()

    @api.one
    def mutation_ok(self):
        old_ids = self.old_owner_ids.ids
        new_ids = self.new_owner_ids.ids

        lots = [lot_id.id for lot_id in self.lot_ids]

        self.change_to_old_owner(old_ids, lots, self.mutation_date)
        self.new_owner_lot(self.lot_ids, new_ids)

        if self.check_last_lot(old_ids):
            self.remove_access_users(old_ids)

        self.state = 'done'
