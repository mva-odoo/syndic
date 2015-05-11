# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from random import randint

class res_users(models.Model):
    _inherit = 'res.users'
    proprio_id = fields.Many2one('syndic.owner', string='ref proprio')


class city(models.Model):
    _name = 'city'
    name = fields.Char('Ville')
    _order = 'name'

class res_partner_address(models.Model):
    _name = 'partner.address'
    city_id = fields.Many2one('city','Ville')
    partner_id = fields.Many2one('res.partner', 'Partner Name', ondelete='set null')
    type = fields.Selection([('default', 'Default'), ('invoice', 'Invoice'), (
        'delivery', 'Delivery'), ('contact', 'Contact'), ('other', 'Other')],
        string='Address Type',
        help="Used to select automatically the right address according to the context in sales and purchases documents.")
    function = fields.Char('Function')
    title = fields.Many2one('res.partner.title', 'Title')
    name = fields.Char('Nom', select=1)
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
    birthdate = fields.Char('Birthdate')
    is_customer_add = fields.Boolean(related='partner_id.customer', string='Customer')
    is_supplier_add = fields.Boolean(related='partner_id.supplier', string='Supplier')
    active = fields.Boolean('Active', help="Uncheck the active field to hide the contact.", default=True)
    company_id = fields.Many2one('res.company', 'Company', select=1)
    color = fields.Integer('Color Index')
    add_parent_id_owner = fields.Many2one('syndic.owner', 'Proprietaire')
    add_parent_id_supplier = fields.Many2one('syndic.owner', 'Fournisseur')
    supplier_id = fields.Many2one('syndic.supplier', 'Fournisseur')
    add_parent_id_loaner = fields.Many2one('syndic.loaner', 'Locataire')
    is_letter = fields.Boolean('Lettre')


class personne(models.Model):
    _name='syndic.personne'
    name = fields.Char('Nom', size=128, required=True, select=True)
    date = fields.Date('Date', select=1)
    title = fields.Many2one('res.partner.title', 'Title')
    active = fields.Boolean('Active', default=True)
    street = fields.Char('Street', size=128)
    street2 = fields.Char('Street2', size=128)
    zip = fields.Char('Zip', change_default=True, size=24)
    city = fields.Char('City', size=128)
    state_id = fields.Many2one("res.country.state", 'State', ondelete='restrict')
    country_id = fields.Many2one('res.country', 'Country', ondelete='restrict')
    email = fields.Char('Email', size=240)
    phone = fields.Char('Phone', size=64)
    fax = fields.Char('Fax', size=64)
    mobile = fields.Char('Mobile', size=64)
    birthdate = fields.Char('Birthdate', size=64)
    city_id = fields.Many2one('city', 'Ville')
    prenom = fields.Char('Prenom')
    image_medium = fields.Binary('medium')
    image_small = fields.Binary('small')
    gsm = fields.Char('GSM')


class res_partner(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    city_id = fields.Many2one('city', 'Ville')
    prenom = fields.Char('Prenom')
    image_medium = fields.Binary('medium')
    image_small = fields.Binary('small')
    gsm = fields.Char('GSM')


#fournisseur   
class Supplier(models.Model):
    _inherit = 'syndic.personne'
    _name='syndic.supplier'
    job_ids = fields.Many2many('res.partner.job', string='Métier')
    address_ids = fields.One2many('partner.address', 'supplier_id', string='Address')

#divers
class Other(models.Model):
    _inherit ='syndic.personne'
    _name = 'syndic.other'

#locataire
class Loaner(models.Model):
    _inherit = 'syndic.personne'
    _name='syndic.loaner'
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

        group_ids = self.env['res.groups'].search(['|', ('name', 'ilike', 'Syndic/Client'), ('name', 'ilike', 'Portal')])
        dict_users['groups_id'] = [(4, group_id.id) for group_id in group_ids]
        self.env.uid = 1
        res_id.user_id = self.env['res.users'].create(dict_users)
        return res_id

    @api.one
    def unlink(self):
        for prop in self:
            prop.user_id.unlink()
        return super(Owner, self).unlink()

#metier  
class res_partner_job(models.Model):
    _name = 'res.partner.job'
    name = fields.Char('Métier')
    _order = 'name'

class res_old_owner(models.Model):
    _name = 'syndic.old.owner'
    _rec_name = 'proprio_id'
    proprio_id = fields.Many2one('syndic.owner', 'Ancien propriétaire')
    lot_ids = fields.Many2many('syndic.lot', string='Lot modifié')
    date_close = fields.Date('Date de fin')


class country(models.Model):
    _inherit = 'res.country'
    _order = 'name asc'


class title(models.Model):
    _inherit = 'res.partner.title'
    _order = 'name'