# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.addons.syndic_tools.syndic_tools import SyndicTools, _MONTH



class Building(models.Model):
    _name = 'syndic.building'
    _description = 'syndic.building'
    _order = 'name asc'

    name = fields.Char('Immeuble', required=True)
    lot_ids = fields.One2many('syndic.lot', 'building_id', 'Lots')
    BCE = fields.Char('BCE')
    num_building = fields.Integer(u"N°", required=True)
    address_building = fields.Char('Rue', required=True)
    zip_building = fields.Integer('Code Postal', required=True)
    city_building = fields.Many2one('res.city', 'Commune', required=True)
    supplier_ids = fields.Many2many('res.partner', 'syndic_building_supplier_rel', string="Fiche technique")

    bank_ids = fields.One2many('res.partner.bank', 'building_id', 'Compte Bancaire')
    total_quotites = fields.Float(compute='_get_total_quotites', string='Total Quotites')
    active = fields.Boolean(default=True)
    fiche_signalitic_ids = fields.One2many(
        'building.signalitic',
        'building_id',
        string='Fiche Signalitique',
        readonly=True
    )  # One2many but it is a relation o2o

    ag_month = fields.Selection(_MONTH, string='Mois')
    ag_fortnight = fields.Selection([('1', '1'), ('2', '2')], string='Quinzaine')
    note = fields.Text('Notes')
    user_id = fields.Many2one('res.users', 'Utilisateur', required=True)
    password = fields.Char('Mot de Passe')
    lot_count = fields.Integer(compute='_get_quotity', string='Nombre de lots')

    owner_count = fields.Integer(compute='_get_quotity', string='Nombre de Propriétaires')
    loaner_count = fields.Integer(compute='_get_quotity', string='Nombre de Locataires')
    honoraire = fields.Float('Honoraire', groups='syndic_base.syndic_manager')
    frais_admin = fields.Float('Frais Administratif', groups='syndic_base.syndic_manager')

    manager_id = fields.Many2one(
        'res.users', 'Manager',
        domain="[('groups_id.name','in',['Syndic/Employe','Syndic/Manager'])]")

    is_lock = fields.Boolean('Bloquer')

    is_building = fields.Boolean('Est un immeuble', default=True)

    def _get_total_quotites(self):
        for building in self:
            building.total_quotites = sum(building.lot_ids.mapped('quotities'))

    def open_sign(self):
        res_id = self.env['building.signalitic'].search([('building_id', '=', self.id)])
        return {
            'res_id': res_id.id,
            'name': 'Ouvrir fiche signalétique',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'building.signalitic',
            'type': 'ir.actions.act_window',
            'context': self._context,
        }

    @api.onchange('zip')
    def _onchange_zip(self):
        return {
            'domain': {'city_id': [('zipcode', '=', self.zip)]}
        }

    def toggle_active(self):
        self.ensure_one()
        self.active = False if self.active else True

    def toggle_lock(self):
        self.ensure_one()
        self.is_lock = False if self.is_lock else True

    def action_inhabitant(self):
        self.ensure_one()
        owner = self.mapped('lot_ids').mapped('owner_ids')
        loaner = self.mapped('lot_ids').mapped('loaner_ids')
        if self._context.get('inhabitant_type') == 'owner':
            action = self.env.ref('syndic_base.action_proprietaire').read()[0]
            action['domain'] = [('id', 'in', owner.ids)]
        elif self._context.get('inhabitant_type') == 'loaner':
            action = self.env.ref('syndic_base.action_locataire').read()[0]
            action['domain'] = [('id', 'in', loaner.ids)]
        else:
            action = self.env.ref('base.action_partner_form').read()[0]
            action['domain'] = [('id', 'in', (owner | loaner).ids)]
            action['context'] = False

        return action

    def action_lot(self):
        self.ensure_one()
        action = self.env.ref('syndic_base.action_lot').read()[0]
        action['domain'] = [('id', '=', self.lot_ids.ids)]
        return action

    def _get_quotity(self):
        for building in self:
            building.lot_count = len(building.lot_ids)
            building.owner_count = len(building.mapped('lot_ids.owner_ids'))
            building.loaner_count = len(building.mapped('lot_ids.loaner_ids'))

    @api.model
    def create(self, vals):
        passwd = vals.get('password') or SyndicTools().pass_generator()

        vals['user_id'] = self.env['res.users'].sudo().create({
            'name': vals['name'],
            'login': vals['name'],
            'password': passwd,
            'groups_id': [(6, 0, self.env['res.groups'].search([('name', 'ilike', 'Syndic/Client')]).ids)],
        }).id

        vals['password'] = passwd
        res = super(Building, self).create(vals)
        self.env['building.signalitic'].create({'building_id': res.id})
        res.user_id.immeuble_id = res.id
        return res

    def write(self, vals):
        if vals.get('name'):
            self.user_id.name = self.user_id.login = vals['name']

        if vals.get('password') and self.user_id:
            self.user_id.password = vals.get('password')

        return super(Building, self).write(vals)

    def unlink(self):
        for building in self:
            building.user_id.unlink()
        return super(Building, self).unlink()


class BuildingUser(models.Model):
    _inherit = 'res.users'

    immeuble_id = fields.Many2one('syndic.building', 'immeuble_id')
