# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions

class mutation(models.Model):
    _name = 'syndic.mutation'
    mutation_date = fields.Date('Date de mutation')
    old_owner_id = fields.Many2one('syndic.owner', 'Ancien Propriétaire', required=True)
    new_owner_id = fields.Many2one('syndic.owner', 'Nouveau Propriétaire', required=True)
    lot_ids = fields.Many2many('syndic.lot', string='Lot', required=True)
    state = fields.Selection([('draft', 'brouillon'), ('done', 'terminé')], 'Etat', default='draft')
    immeuble_id = fields.Many2one('syndic.building', related='lot_ids.building_id', store=True, string="Immeuble")

    @api.one
    def new_owner_lot(self, lots, new_id):
        lots.write({'proprio_id': [(6, 0, [new_id])]})

    @api.one
    def check_last_lot(self, old_id):
        res = False
        if not self.env['syndic.lot'].search([('proprio_id', '=', old_id)]):
            res = True
        return res

    @api.one
    def change_to_old_owner(self, old_id, lots, mutation_date):
        vals = {'proprio_id': old_id, 'lot_ids': [(6, 0, lots)], 'date_close': mutation_date}
        self.env['syndic.old.owner'].create(vals)

    @api.one
    def remove_access_users(self, old_id):
        user_ids = self.env['res.users'].search([('proprio_id', '=', old_id)])
        user_ids.unlink()

    @api.one
    def mutation_ok(self):
        old_id = self.old_owner_id.id
        new_id = self.new_owner_id.id

        # make a list of lot
        lots = [lot_id.id for lot_id in self.lot_ids]

        self.change_to_old_owner(old_id, lots, self.mutation_date)
        self.new_owner_lot(self.lot_ids, new_id)

        if self.check_last_lot(old_id):
            self.remove_access_users(old_id)

        self.state = 'done'