# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class Mutation(models.Model):
    _name = 'syndic.mutation'
    _description = 'syndic.mutation'
    _order = 'immeuble_id'

    name = fields.Char('Mutation', compute='_get_name', store=True)
    mutation_date = fields.Date('Date de mutation', required=True)
    old_partner_ids = fields.Many2many(
        'res.partner',
        'old_mutation_rel',
        string=u'Ancien Propriétaire',
        required=True
    )
    new_owner_id = fields.Many2one('res.partner', 'Nouveau Propriétaire', required=True)
    lot_ids = fields.Many2many('syndic.lot', string='Lot', required=True)
    state = fields.Selection([('draft', 'brouillon'), ('done', 'terminé')], 'Etat', default='draft')
    immeuble_id = fields.Many2one('syndic.building', related='lot_ids.building_id', store=True, string="Immeuble")
    note = fields.Text('Note')
    new_partner_ids = fields.Many2many(
            'res.partner',
            'new_mutation_rel',
            string=u'Nouveaux Propriétaire',
    )

    @api.depends('old_partner_ids', 'new_owner_id')
    def _get_name(self):
        for mutation in self:
            mutation.name = 'Mutation de %s vers %s' % (
                ''.join(mutation.old_partner_ids.mapped('name') or []),
                mutation.new_owner_id.name or '',
            )

    @api.onchange('old_partner_ids')
    def onchange_old_owner(self):
        return {
            'domain': {'lot_ids': [('owner_id', 'in',  self.old_partner_ids.ids)]}
        }

    def mutation(self):
        self.ensure_one()
        self.lot_ids.write({'owner_id': self.new_owner_id.id})

        if not self.old_partner_ids.mapped('lot_ids.owner_id'):
            self.old_partner_ids.mapped('user_id').write({'active': False})

        self.state = 'done'
