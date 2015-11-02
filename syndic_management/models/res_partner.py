# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from openerp.addons.syndic_tools.syndic_tools import UCLTools


class ResUsers(models.Model):
    _inherit = 'res.users'

    proprio_id = fields.Many2one('syndic.owner', string='ref proprio')


class City(models.Model):
    _name = 'city'
    _order = 'name'

    name = fields.Char('Ville', required=True)


class ResPartnerAddress(models.Model):
    _name = 'partner.address'

    name = fields.Char('Nom', select=1, required=True)
    city_id = fields.Many2one('city', 'Ville')
    title = fields.Many2one('res.partner.title', 'Title')
    street = fields.Char('Rue')
    street2 = fields.Char('Rue2')
    zip = fields.Char('Code Postal', change_default=True)
    city = fields.Char('Ville')
    state_id = fields.Many2one("res.country.state", 'Fed. State', domain="[('country_id','=',country_id)]")
    country_id = fields.Many2one('res.country', 'Country')
    email = fields.Char('E-Mail')
    phone = fields.Char('Phone')
    fax = fields.Char('Fax')
    mobile = fields.Char('Mobile')
    active = fields.Boolean('Active', help="Uncheck the active field to hide the contact.", default=True)
    add_parent_id_owner = fields.Many2one('syndic.owner', 'Proprietaire')
    add_parent_id_supplier = fields.Many2one('syndic.owner', 'Fournisseur')
    supplier_id = fields.Many2one('syndic.supplier', 'Fournisseur')
    add_parent_id_loaner = fields.Many2one('syndic.loaner', 'Locataire')
    is_letter = fields.Boolean('Lettre')


class Person(models.Model):
    _name = 'syndic.personne'

    name = fields.Char('Nom', select=1, required=True)
    title = fields.Many2one('res.partner.title', 'Title')
    active = fields.Boolean('Active', default=True)
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", 'State', ondelete='restrict')
    country_id = fields.Many2one('res.country', 'Country', ondelete='restrict')
    email = fields.Char('Email')
    phone = fields.Char('Phone')
    fax = fields.Char('Fax')
    mobile = fields.Char('Mobile')
    city_id = fields.Many2one('city', 'Ville')
    prenom = fields.Char('Prenom')
    gsm = fields.Char('GSM')
    user_id = fields.Many2one('res.users', string="User", ondelete="cascade")


# fournisseur
class Supplier(models.Model):
    _inherit = 'syndic.personne'
    _name = 'syndic.supplier'

    job_ids = fields.Many2many('res.partner.job', string='Métier')
    address_ids = fields.One2many('partner.address', 'supplier_id', string='Address')


# locataire
class Loaner(models.Model):
    _inherit = 'syndic.personne'
    _name = 'syndic.loaner'

    address_ids = fields.One2many('partner.address', 'add_parent_id_loaner', string='Address')
    loaner_lot_ids = fields.Many2many('syndic.lot', string='Lot')
    login = fields.Char('login')
    passcode = fields.Char('passcode')
    building_ids = fields.Many2one('syndic.building', related='loaner_lot_ids.building_id', string='Immeuble')
    building_store_ids = fields.Many2one('syndic.building', related='loaner_lot_ids.building_id',
                                         string='Immeuble', store=True)


class Owner(models.Model):
    _inherit = 'syndic.personne'
    _name = 'syndic.owner'

    address_ids = fields.One2many('partner.address', 'add_parent_id_owner', string='Address')
    lot_ids = fields.Many2many('syndic.lot', string='Lot')
    login = fields.Char('login', related='user_id.login', required=False)
    password = fields.Char('Mot de passe', related='user_id.password')
    building_ids = fields.Many2one('syndic.building', related='lot_ids.building_id', string='Immeuble')
    building_store_ids = fields.Many2one('syndic.building', related='lot_ids.building_id',
                                         string='Immeuble', store=True)
    convocation = fields.Selection([('recommende', 'Par recommandé'),
                                    ('courrier_simple', 'Par courrier simple'),
                                    ('email', 'Par Email')], string='Convocation')

    @api.model
    def create(self, vals):
        res_id = super(Owner, self).create(vals)
        if res_id.user_id:
            group_ids = self.env['res.groups'].search(['|',
                                                       ('name', 'ilike', 'Syndic/Client'),
                                                       ('name', 'ilike', 'Portal')
                                                       ])

            dict_users = {
                'name': vals['name'],
                'login': UCLTools().login_generator(vals['name']),
                'password': UCLTools().pass_generator(),
                'proprio_id': res_id.id,
                'groups_id': [(4, group_id.id) for group_id in group_ids],
            }

            res_id.user_id = self.env['res.users'].sudo().create(dict_users)
        return res_id

    @api.one
    def unlink(self):
        self.user_id.unlink()
        return super(Owner, self).unlink()


# metier
class ResPartnerJob(models.Model):
    _name = 'res.partner.job'
    _order = 'name'

    name = fields.Char('Métier', requiered=True)


class ResOldOwner(models.Model):
    _name = 'syndic.old.owner'
    _rec_name = 'proprio_id'

    proprio_id = fields.Many2one('syndic.owner', 'Ancien propriétaire', required=True)
    lot_ids = fields.Many2many('syndic.lot', string='Lot modifié')
    date_close = fields.Date('Date de fin')


class Country(models.Model):
    _inherit = 'res.country'
    _order = 'name asc'


class Title(models.Model):
    _inherit = 'res.partner.title'
    _order = 'name'