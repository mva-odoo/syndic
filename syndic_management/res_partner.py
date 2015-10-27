# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from random import randint
import random

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

    name = fields.Char('Nom', required=True, select=True)
    date = fields.Date('Date', select=1)
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
    birthdate = fields.Char('Birthdate')
    city_id = fields.Many2one('city', 'Ville')
    prenom = fields.Char('Prenom')
    image_medium = fields.Binary('medium')
    image_small = fields.Binary('small')
    gsm = fields.Char('GSM')


# fournisseur
class Supplier(models.Model):
    _inherit = 'syndic.personne'
    _name='syndic.supplier'

    job_ids = fields.Many2many('res.partner.job', string='Métier')
    address_ids = fields.One2many('partner.address', 'supplier_id', string='Address')


#divers
#TODO aucune utilité ???
class Other(models.Model):
    _inherit ='syndic.personne'
    _name = 'syndic.other'


#locataire
class Loaner(models.Model):
    _inherit = 'syndic.personne'
    _name = 'syndic.loaner'

    address_ids = fields.One2many('partner.address','add_parent_id_loaner',string='Address')
    loaner_lot_ids = fields.Many2many('syndic.lot',string='Lot')
    login = fields.Char('login')
    passcode = fields.Char('passcode')
    building_ids = fields.Many2one('syndic.building', related='loaner_lot_ids.building_id', string='Immeuble')
    building_store_ids = fields.Many2one('syndic.building', related='loaner_lot_ids.building_id',
                                         string='Immeuble', store=True)


#propriétaire
class Owner(models.Model):
    _inherit = 'syndic.personne'
    _name = 'syndic.owner'

    #TODO enlever ???
    # @api.model
    # def _get_name_building(self):
    #     result = set()
    #     building_ids = self.env['syndic.owner'].search([])
    #     for el in building_ids:
    #         result.add(el.id)
    #     return list(result)

    address_ids = fields.One2many('partner.address', 'add_parent_id_owner',string='Address')
    lot_ids = fields.Many2many('syndic.lot', string='Lot')
    login = fields.Char('login', related='user_id.login')
    password = fields.Char('Mot de passe', related='user_id.password')
    building_ids = fields.Many2one('syndic.building', related='lot_ids.building_id', string='Immeuble')
    # building_store_ids = fields.Many2one('syndic.building', related='lot_ids.building_id', string='Immeuble', store={
    #     'syndic.lot': (_get_name_building, ['name'], 10),
    #     'syndic.owner': (lambda self, cr, uid, ids, c=None: ids, [], 10),
    # }, select=True)
    convocation = fields.Selection([('recommende', 'Par recommandé'),
                                    ('courrier_simple', 'Par courrier simple'),
                                    ('email', 'Par Email')], string='Convocation')
    building_store_ids = fields.Many2one('syndic.building', related='lot_ids.building_id', string='Immeuble', store=True)
    user_id = fields.Many2one('res.users', string="User")

    #TODO: deplacer dans un module à part comme utils
    def pass_generator(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pw_length = 8
        mypw = ""

        for i in range(pw_length):
            next_index = random.randrange(len(alphabet))
            mypw = mypw + alphabet[next_index]

        return mypw

    @api.model
    def create(self, vals):
        res_id = super(Owner, self).create(vals)
        login = vals['name'].replace(' ', '')
        login = login.replace('-', '')
        rand = str(randint(0, 99))
        dict_users = {}
        dict_users['login'] = login[:8]+rand
        dict_users['password'] = self.pass_generator()
        dict_users['name'] = vals['name']
        dict_users['proprio_id'] = res_id.id

        group_ids = self.env['res.groups'].search(['|',
                                                   ('name', 'ilike', 'Syndic/Client'),
                                                   ('name', 'ilike', 'Portal')
                                                   ])

        dict_users['groups_id'] = [(4, group_id.id) for group_id in group_ids]
        self.env.uid = 1
        res_id.user_id = self.env['res.users'].create(dict_users)
        return res_id

    @api.one
    def unlink(self):
        #TODO louche de boucler sur self avec api.one
        for prop in self:
            prop.user_id.unlink()
        return super(Owner, self).unlink()


#metier  
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
