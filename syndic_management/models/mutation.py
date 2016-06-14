# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Mutation(models.Model):
    _name = 'syndic.mutation'
    _order = 'immeuble_id'

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
    def mutation(self):
        for old_id in self.old_owner_ids:
            self.env['syndic.old.owner'].create({
                'proprio_id': old_id.id,
                'lot_ids': [(6, 0, self.lot_ids.ids)],
                'date_close': self.mutation_date,
            })

        self.lot_ids.write({'proprio_id': [(6, 0, self.new_owner_ids.ids)]})

        if not self.old_owner_ids.mapped('lot_ids.proprio_id'):
            self.old_owner_ids.mapped('user_id').write({'active': False})

        self.state = 'done'
