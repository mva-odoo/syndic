# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, SUPERUSER_ID


class Partner(models.Model):
    _inherit = 'res.partner'

    is_loaner = fields.Boolean('Locataire', compute='_get_partner_type', store=True)
    is_owner = fields.Boolean('Propriétaire', compute='_get_partner_type', store=True)
    is_old = fields.Boolean('Ancien propriétaire', compute='_get_partner_type', store=True)

    # TODO: check to replace with supplier_rank but need account
    supplier = fields.Boolean('Supplier')

    mobile = fields.Char('GSM')
    fax = fields.Char('fax')

    job_ids = fields.Many2many('res.partner.job', string='Métier(s)')

    first_name = fields.Char('Prénom')
    convocation = fields.Selection([
        ('recommende', 'Par recommandé'),
        ('courrier_simple', 'Par courrier simple'),
        ('email', 'Par Email')
    ], string='Convocation')

    is_letter = fields.Boolean('Par Lettre')
    is_email = fields.Boolean('Par Email')

    lot_ids = fields.One2many('syndic.lot', 'owner_id', 'Lots')
    lot_count = fields.Integer('Quotitees Totales', compute='_get_number_lot')

    loaner_lot_ids = fields.Many2many('syndic.lot', 'syndic_lot_loan_rel', string='Lots(Locataire)')
    loaner_lot_count = fields.Integer('nombre Lots(Locataire)', compute='_get_number_lot_loaner')
    old_lot_count = fields.Integer('Mutations', compute='_get_old_lot_owner')

    owner_building_ids = fields.Many2many(
        'syndic.building',
        compute='_get_building',
        search='_search_building',
        string='Immeuble'
    )
    loaner_building_ids = fields.Many2many(
        'syndic.building',
        compute='_get_building',
        search='_search_loaner_building',
        string='Immeuble(Locataire)'
    )

    country_id = fields.Many2one('res.country', default=lambda s: s.env.ref('base.be'))

    def name_get(self):
        result = []
        for partner in self:
            if partner.first_name:
                name = partner.name + '-' + partner.first_name
            else:
                name = partner.name
            result.append((partner.id, name))
        return result

    def _onchange_city_id(self):
        # remove behavior of the city module
        pass

    #  TODO: understand why ???
    def _get_name(self):
        if self._context.get('standard'):
            return super(Partner, self)._get_name()
        return self.name

    def _get_old_lot_owner(self):
        for partner in self:
            partner.old_lot_count = self.env['syndic.mutation'].search_count([
                ('state', '=', 'done'),
                ('old_partner_ids', 'in', partner.id)
            ])

    @api.depends('lot_ids')
    def _get_number_lot(self):
        for partner in self:
            partner.lot_count = len(partner.lot_ids)

    @api.depends('loaner_lot_ids')
    def _get_number_lot_loaner(self):
        for partner in self:
            partner.loaner_lot_count = len(partner.loaner_lot_ids)

    def _search_building(self, operator, value):
        field = 'lot_ids.building_id.name'
        if isinstance(value, int):
            field = 'lot_ids.building_id.id'
        return [(field, operator, value)]

    def _search_loaner_building(self, operator, value):
        return [('loaner_lot_ids.building_id.id', operator, value)]

    def _get_building(self):
        for partner in self:
            partner.owner_building_ids = partner.lot_ids.mapped('building_id')
            partner.loaner_building_ids = partner.loaner_lot_ids.mapped('building_id')

    @api.model
    def create(self, vals):
        partner = super(Partner, self).create(vals)
        if not self._context.get('normal_create'):
            self.env['res.users'].with_context(normal_create=False, no_reset_password=True).create({
                'partner_id': partner.id,
                'name': partner.name,
                'login': '%s - %s' % (partner.name, partner.id),
                # 'company_id': partner.company_id.id,
                # 'company_ids': [(4, partner.company_id.id)],
                'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])]
            })
        return partner

    def write(self, vals):
        # if vals.get('company_id') and vals['company_id'] != 1:
        #     del vals['company_id']
        return super().write(vals)

    @api.depends(
        'lot_ids',
        'loaner_lot_ids',
        'loaner_lot_ids.building_id.active',
        'lot_ids.building_id.active',
        'lot_ids.mutation_ids'
    )
    def _get_partner_type(self):
        for partner in self:
            mutations = self.env['syndic.mutation'].search([('state', '=', 'done')])
            partner.is_owner = True if partner.lot_ids.filtered(lambda s: s.building_id.active) else False
            partner.is_old = True if not partner.is_owner and partner.lot_ids.filtered(lambda s: not s.building_id.active) or partner in mutations.old_partner_ids else False
            partner.is_loaner = True if partner.loaner_lot_ids and partner.loaner_lot_ids.filtered(lambda s: s.building_id.active) else False

    # TODO : clean
    @api.onchange('zip', 'country_id')
    def _onchange_zip(self):
        domain = [('country_id', '=', self.country_id.id)]
        if self.country_id.id == self.env.ref('base.be').id:
            domain.append(('zipcode', '=', self.zip))
        return {
            'domain': {'city_id': domain}
        }

    def action_lot(self):
        self.ensure_one()
        action = self.env.ref('syndic_base.action_lot').sudo().read()[0]
        action['domain'] = [('id', 'in', self.lot_ids.ids)]
        return action

    def action_lot_loaner(self):
        self.ensure_one()
        action = self.env.ref('syndic_base.action_lot').sudo().read()[0]
        action['domain'] = [('id', 'in', self.loaner_lot_ids.ids)]
        return action

    def action_lot_old(self):
        self.ensure_one()
        action = self.env.ref('syndic_base.action_mutation').sudo().read()[0]
        action['domain'] = [('old_partner_ids', 'in', self.id)]
        return action


class Title(models.Model):
    _inherit = 'res.partner.title'
    _order = 'name'


class Country(models.Model):
    _inherit = 'res.country'
    _order = 'name asc'
