# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from openerp.addons.syndic_tools.syndic_tools import SyndicTools


class ResUsers(models.Model):
    _inherit = 'res.users'

    proprio_id = fields.Many2one('syndic.owner', string='ref proprio')
    server_mail_id = fields.Many2one('ir.mail_server', 'Serveur Email')


class City(models.Model):
    _name = 'city'
    _order = 'name'

    name = fields.Char('Ville', required=True)
    zip = fields.Char('Code Postal')
    country_id = fields.Many2one('res.country', 'Country')
    active = fields.Boolean('Actif', default=True)

    @api.model
    def create(self, vals):
        if vals.get('name'):
            vals['name'] = vals['name'][0].upper()+vals['name'][1:].lower()
        return super(City, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('name'):
            vals['name'] = vals['name'][0].upper()+vals['name'][1:].lower()
        return super(City, self).write(vals)


class ResPartnerAddress(models.Model):
    _name = 'partner.address'

    name = fields.Char('Nom', index=1, required=True)
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
    is_email = fields.Boolean('Email')


class Person(models.Model):
    _name = 'syndic.personne'
    _order = 'name'

    name = fields.Char('Nom', index=1, required=True)
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

    address_ids = fields.One2many('partner.address', 'add_parent_id_loaner', string='Adresse')
    loaner_lot_ids = fields.Many2many('syndic.lot', string='Lot')
    login = fields.Char('login')
    passcode = fields.Char('passcode')
    building_ids = fields.Many2one('syndic.building', related='loaner_lot_ids.building_id', string='Immeuble non-storé')
    building_store_ids = fields.Many2one('syndic.building', related='loaner_lot_ids.building_id',
                                         string='Immeuble', store=True)


class Owner(models.Model):
    _inherit = 'syndic.personne'
    _name = 'syndic.owner'

    # def _auto_init(self):
    #     def _get_fk_on(table):
    #         """ return a list of many2one relation with the given table.
    #             :param table : the name of the sql table to return relations
    #             :returns a list of tuple 'table name', 'column name'.
    #         """
    #         query = """
    #             SELECT cl1.relname as table, att1.attname as column
    #             FROM pg_constraint as con, pg_class as cl1, pg_class as cl2, pg_attribute as att1, pg_attribute as att2
    #             WHERE con.conrelid = cl1.oid
    #                 AND con.confrelid = cl2.oid
    #                 AND array_lower(con.conkey, 1) = 1
    #                 AND con.conkey[1] = att1.attnum
    #                 AND att1.attrelid = cl1.oid
    #                 AND cl2.relname = %s
    #                 AND att2.attname = 'id'
    #                 AND array_lower(con.confkey, 1) = 1
    #                 AND con.confkey[1] = att2.attnum
    #                 AND att2.attrelid = cl2.oid
    #                 AND con.contype = 'f'
    #         """
    #         self._cr.execute(query, (table,))
    #         return self._cr.fetchall()
    #
    #     for fk in _get_fk_on(self._table):
    #         table, col = fk
    #         self._cr.execute('ALTER TABLE %s ADD COLUMN %s INTEGER;' % fk)
    #         partner_id = False
    #         fields_to_export = []
    #
    #         dict_fields = self.fields_get()
    #         for field in dict_fields:
    #             if dict_fields[field]['type'] not in ['many2many', 'one2many']:
    #                 fields_to_export.append(field)
    #
    #         for owner in self.search([]):
    #             datas = self.read([fields_to_export])[0]
    #             if owner.user_id:
    #                 if owner.user_id.partner_id:
    #                     partner_id = owner.user_id.partner_id.write(datas)
    #
    #             if not partner_id:
    #                 partner_id = self.env['res.partner'].create(datas)
    #
    #             self._cr.execute('UPDATE % SET %s=%s; where %s=%s;', (table, col, partner_id.id, col, self.id))

    address_ids = fields.One2many('partner.address', 'add_parent_id_owner', string='Address')
    lot_ids = fields.Many2many('syndic.lot', string='Lot')
    login = fields.Char('login', related='user_id.login', required=False)
    password = fields.Char('Mot de passe généré', info="Il se peut que l\'utilisateur ai changé de mot de passe dans"
                                                       "ce cas il le mot de passe peut etre regeneré")
    building_ids = fields.Many2one('syndic.building', related='lot_ids.building_id', string='Immeuble')
    building_store_ids = fields.Many2one('syndic.building', related='lot_ids.building_id',
                                         string='Immeuble', store=True)
    convocation = fields.Selection([('recommende', 'Par recommandé'),
                                    ('courrier_simple', 'Par courrier simple'),
                                    ('email', 'Par Email')], string='Convocation')

    def sgimmo_check_login_unicity(self, login):
        if self.env['res.users'].search_count([('login', '=', login)]):
            return False
        return True

    @api.model
    def create(self, vals):
        res_id = super(Owner, self).create(vals)
        login = SyndicTools().login_generator(vals['name'])
        if self.sgimmo_check_login_unicity(login):
            # group_ids = self.env['res.groups'].search([('name', 'ilike', 'Syndic/Client')])

            dict_users = {
                'name': vals['name'],
                'login': login,
                'password': SyndicTools().pass_generator(),
                'proprio_id': res_id.id,
                'groups_id': [(6, 0, self.env.ref('syndic_management.syndic_client').ids)],
            }

            self.write({
                'user_id': self.env['res.users'].sudo().create(dict_users),
                'password': dict_users['password']
            })
        return res_id

    @api.one
    def change_password(self):
        if self.user_id:
            dict_users = {
                'login': SyndicTools().login_generator(self.name),
                'password': SyndicTools().pass_generator(),
            }
            self.user_id.sudo().write(dict_users)
            self.password = dict_users['password']
        else:
            user = self.env['res.users'].sudo().create({
                'name': self.name,
                'login': SyndicTools().login_generator(self.name),
                'password': SyndicTools().pass_generator(),
                'proprio_id': self.id,
                'groups_id': [(6, 0, self.env.ref('syndic_management.syndic_client').ids)],
            })

            self.write({
                'user_id': user.id,
                'password': user.password
            })

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
    _order = 'proprio_id'

    proprio_id = fields.Many2one('syndic.owner', 'Ancien propriétaire', required=True)
    lot_ids = fields.Many2many('syndic.lot', string='Lot modifié')
    date_close = fields.Date('Date de fin')


class Country(models.Model):
    _inherit = 'res.country'
    _order = 'name asc'


class Title(models.Model):
    _inherit = 'res.partner.title'
    _order = 'name'
