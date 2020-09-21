# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.addons.syndic_tools.syndic_tools import SyndicTools, _MONTH


class Building(models.Model):
    _name = 'syndic.building'
    _inherit = 'barcode.import'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'syndic.building'
    _order = 'name asc'

    _print_barcode = False
    _building_field = 'id'
    _barcode_type = 'immeuble'

    lot_ids = fields.One2many('syndic.lot', 'building_id', 'Lots')
    BCE = fields.Char('BCE')
    num_building = fields.Integer(u"N°", required=True)
    supplier_ids = fields.Many2many('res.partner', 'syndic_building_supplier_rel', string="Fiche technique")

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
    note = fields.Text('Note')
    password = fields.Char('Mot de Passe')
    lot_count = fields.Integer(compute='_get_quotity', string='Nombre de lots')

    partner_id = fields.Many2one('res.partner', 'Contact Immeuble', ondelete='cascade', required=True)

    owner_count = fields.Integer(compute='_get_quotity', string='Nombre de Propriétaires')
    loaner_count = fields.Integer(compute='_get_quotity', string='Nombre de Locataires')

    contract_count = fields.Integer(compute='_get_contract', string='Nombre de Contrat')

    # TODO: remove after honoraire
    honoraire = fields.Float('Honoraire', groups='syndic_base.syndic_manager')
    frais_admin = fields.Float('Frais Administratif', groups='syndic_base.syndic_manager')

    contrat_ids = fields.One2many('syndic.building.contract', 'building_id', 'Contrats')

    manager_id = fields.Many2one(
        'res.users', 'Manager',
        domain="[('groups_id.name','in',['Syndic/Employe','Syndic/Manager'])]")

    is_lock = fields.Boolean('Bloquer')

    is_building = fields.Boolean('Est un immeuble', default=True)

    quotity_type_ids = fields.Many2many('syndic.building.quotities.type', string='Type de quotitées')
    quotity_ids = fields.Many2many(
        'syndic.building.quotities',
        string='Quotitées',
    )

    def get_quotities(self):
        quotity = self.env['syndic.building.quotities']
        for rec in self:
            rec.quotity_ids = quotity.browse([
                quotity.new({
                    'lot_id': lot.id,
                    'quotity_type_id': quotity_type.id,
                    'quotities': lot.quotities
                }).id
                for lot in rec.lot_ids
                for quotity_type in rec.quotity_type_ids
            ])

    def name_get(self):
        return [[rec.id, '%s-%s' % (rec.num_building, rec.name)] for rec in self]

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
        owner = self.mapped('lot_ids.owner_id')
        loaner = self.mapped('lot_ids.loaner_ids')
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
            building.owner_count = len(building.mapped('lot_ids.owner_id'))
            building.loaner_count = len(building.mapped('lot_ids.loaner_ids'))

    def _get_contract(self):
        for building in self:
            building.contract_count = len(building.contrat_ids)

    def action_contract(self):
        self.ensure_one()
        action = self.env.ref('syndic_base.action_building_contract').read()[0]
        action['domain'] = [('building_id', '=', self.id)]
        action['context'] = {'default_building_id': self.id}
        return action

    @api.model
    def create(self, vals):
        res = super(Building, self).create(vals)
        res.partner_id.write({
            'title': self.env.ref('syndic_base.title_acp').id,
        })
        self.env['building.signalitic'].create({'building_id': res.id})
        return res
