# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.addons.syndic_tools.syndic_tools import SyndicTools, _MONTH


class Building(models.Model):
    _name = 'syndic.building'
    _inherit = 'barcode.import'
    _inherits = {'res.company': 'company_id'}
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

    diu_ids = fields.One2many('syndic.building.diu', 'diu_id', 'DIU')
    ag_month = fields.Selection(_MONTH, string='Mois')
    ag_fortnight = fields.Selection([('1', '1'), ('2', '2')], string='Quinzaine')
    note = fields.Text('Note')
    password = fields.Char('Mot de Passe')
    lot_count = fields.Integer(compute='_get_quotity', string='Nombre de lots')

    partner_id = fields.Many2one('res.partner', 'Contact Immeuble',)
    city_id = fields.Many2one(related='partner_id.city_id', string='Ville')
    company_id = fields.Many2one('res.company', 'Société Immeuble', ondelete='cascade', required=True)

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

    # access
    access_info = fields.Text(u'Porte d’entrée: informations et descriptions')
    access_where = fields.Many2one('res.partner', u'Certificat pour la reproduction de clé')
    access_more = fields.Text('Informations et descriptions')

    expert_tech_id = fields.Many2one('res.partner', 'Expert technique', domain=[('supplier', '=', True)])
    expert_chauffage_id = fields.Many2one('res.partner', 'Expert chauffage', domain=[('supplier', '=', True)])
    expert_ascenseur_id = fields.Many2one('res.partner', 'Expert ascenseur', domain=[('supplier', '=', True)])
    conseiller_tech_id = fields.Many2one('res.partner', 'Conseiller technique', domain=[('supplier', '=', True)])
    conseiller_juridique_id = fields.Many2one('res.partner', 'Conseiller juridique', domain=[('supplier', '=', True)])

    amiante_date = fields.Date('Inventaire établi le')
    amiante_partner_id = fields.Many2one('res.partner', 'Inventaire établi le', domain=[('supplier', '=', True)])
    amiante_done = fields.Boolean('Désamiantage réalisé')
    amiante_description = fields.Text('Informations supplémentaires (amiante)')

    status_update = fields.Boolean('Statuts mis à jour')
    roi_update = fields.Boolean('ROI mis à jour')
    status_description = fields.Text('Informations supplémentaires (status)')

    permis_delivre = fields.Date('Délivré le')
    env_validity = fields.Date('Valide jusqu\'au')
    env_description = status_description = fields.Text('Informations supplémentaires (permis d\'environnement)')

    citerne_description = status_description = fields.Char('Contenance et informations')
    citerne_date = status_description = fields.Date('Certificat de conformité établi le')
    citerne_validity = status_description = fields.Date('Certificat de conformité valide jusqu\'au')
    citerne_partner_id = status_description = fields.Many2one('res.partner', 'Certificat de conformité établi par', domain=[('supplier', '=', True)])
    amiante_neutralise = fields.Boolean('Citerne neutralisée')
    pollution_zone = fields.Boolean('Sol en zone polluée')
    depollution = fields.Text('Dépollution')

    analyse_date = fields.Date('Analyse de risque établi le')
    analys_validaty_date = fields.Date('Analyse de risque établi le')
    analyse_partner_id = fields.Many2one('res.partner', 'Analyse de risque établi par', domain=[('supplier', '=', True)])
    ascenseur_conformite = fields.Boolean('Ascenseur mis en conformité')
    attestation_conformite = fields.Boolean('Attestation de conformité reçue')
    attestation_partner_id = fields.Many2one('res.partner', 'Analyse de risque établi par', domain=[('supplier', '=', True)])

    elec_recue = fields.Boolean('Conformité reçue')
    elec_partner_id = fields.Many2one('res.partner', 'Rapport établi par', domain=[('supplier', '=', True)])
    elec_date = fields.Date('Analyse de risque établi le')
    elec_validity = fields.Date('Date echeance')

    peb = fields.Char('Chauffage au norme')

    def get_quotities(self):
        quotity = self.env['syndic.building.quotities']
        for rec in self:
            old_quotity = rec.quotity_ids.filtered(lambda s:s.quotity_type_id in rec.quotity_type_ids)
            (rec.quotity_ids - old_quotity).sudo().unlink()
            new_type = rec.quotity_type_ids - rec.quotity_ids.mapped('quotity_type_id')

            new_quotity = quotity.browse([
                quotity.new({
                    'lot_id': lot.id,
                    'quotity_type_id': quotity_type.id,
                    'quotities': lot.quotities
                }).id
                for lot in rec.lot_ids
                for quotity_type in new_type
            ])

            rec.quotity_ids = new_quotity | old_quotity

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

    def open_description(self):
        res_id = self.env['building.signalitic'].search([('building_id', '=', self.id)])
        view_id = self.env.ref('syndic_base.form_description_building').id
        return {
            'res_id': res_id.id,
            'name': 'Description immeuble',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'view_id': view_id,
            'res_model': 'building.signalitic',
            'type': 'ir.actions.act_window',
            'context': self._context,
        }

    def open_tech(self):
        res_id = self.env['building.signalitic'].search([('building_id', '=', self.id)])
        view_id = self.env.ref('syndic_base.form_tech_building').id
        return {
            'res_id': res_id.id,
            'name': 'Description immeuble',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'view_id': view_id,
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
            action = self.env.ref('syndic_base.action_proprietaire').sudo().read()[0]
            action['domain'] = [('id', 'in', owner.ids)]
        elif self._context.get('inhabitant_type') == 'loaner':
            action = self.env.ref('syndic_base.action_locataire').sudo().read()[0]
            action['domain'] = [('id', 'in', loaner.ids)]
        else:
            action = self.env.ref('base.action_partner_form').sudo().read()[0]
            action['domain'] = [('id', 'in', (owner | loaner).ids)]
            action['context'] = False

        return action

    def action_lot(self):
        self.ensure_one()
        action = self.env.ref('syndic_base.action_lot').sudo().read()[0]
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
        action = self.env.ref('syndic_base.action_building_contract').sudo().read()[0]
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
