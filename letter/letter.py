# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
import datetime
import locale

class piece_jointe(models.Model):
    _name = 'piece.jointe'
    _rec_name = 'attachement_id'
    attachement_id = fields.Many2one('ir.attachment', string='attachement', required=True)
    letter_id = fields.Many2one('letter.create', string='Lettre')


class create_letter(models.Model):
    _name = 'letter.create'
    _rec_name = 'sujet'
    _inherit = 'mail.thread'

    @api.one
    @api.depends('date')
    def _compute_date(self):
        if self.date:
            now = datetime.datetime.strptime(self.date, '%Y-%m-%d')
            try:
                locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')
            except Exception:
                locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')
            date_fr = now.strftime("%A %d %B %Y")
            self.date_fr = date_fr

    name = fields.Char('ID de la lettre', readonly=True)
    sujet = fields.Char('Sujet', required=True)
    immeuble_id = fields.Many2one('syndic.building', string='Immeuble')
    all_immeuble = fields.Boolean('Immeuble entier')
    propr_ids = fields.Many2many('syndic.owner', string='Propriétaire')
    fourn_ids = fields.Many2many('syndic.supplier', string='Fournisseurs')
    divers_ids = fields.Many2many('syndic.other', string='Divers')
    old_ids = fields.Many2many('syndic.old.owner', string='Fournisseurs')
    loc_ids = fields.Many2many('syndic.loaner', string='Locataires')
    end_letter_id = fields.Many2one('letter.end', 'Fin de lettre', required=True)
    begin_letter_id = fields.Many2one('letter.begin', 'Début de lettre', required=True)
    letter_type_id = fields.Many2one('letter.type', 'Type de lettre', required=True)
    letter_model_id = fields.Many2one('letter.model', 'Modèle de lettre')
    contenu = fields.Html('contenu', required=True)
    ps = fields.Text('PS')
    save_letter = fields.Boolean('Sauver la lettre comme modèle')
    name_template = fields.Char('Nom du modèle de lettre')
    is_mail = fields.Boolean('Envoi par email')
    is_fax = fields.Boolean('Envoi par fax')
    piece_jointe_ids = fields.One2many('piece.jointe', 'letter_id', string='Piece Jointe')
    create_date = fields.Datetime('Date de création')
    date = fields.Date('Date de création', default=lambda *a: fields.date.today())
    date_fr = fields.Char(string='Date', compute='_compute_date', store=True)
    partner_address_ids = fields.Many2many('partner.address', String="Personne Jointe")
    state = fields.Selection([('not_send', 'Pas envoyé'), ('send', 'Envoyé')], string='State', default='not_send')
    mail_server = fields.Many2one('ir.mail_server', 'Serveur email')

    _order = 'create_date desc'

    @api.onchange('date')
    def onchange_date(self):
        if self.date:
            now = datetime.datetime.strptime(self.date, '%Y-%m-%d')
            try:
                locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')
            except Exception:
                locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')
            date_fr = now.strftime("%A %d %B %Y")
            self.date_fr = date_fr

    @api.one
    def copy(self, default=None):
        default['date'] = fields.date.today()
        return super(create_letter, self).copy(default)

    @api.model
    def create(self, vals):
        values = {}
        res = super(create_letter, self).create(vals)

        if res.save_letter:
                res.env['letter.model'].create({'name': res.name_template, 'text': res.contenu})

        for supplier_id in res.fourn_ids:
            values['name'] = res.sujet
            values['fournisseur_id'] = supplier_id.id
            if not res.immeuble_id.id:
                raise Exception("Il faut un immeuble pour créer un bon de commande ou une offre")
            values['immeuble_id'] = res.immeuble_id.id
            if res.letter_type_id.name in ['Demande de devis', 'Demande d\'offre', 'Demande de contrat']:
                values['date_envoi'] = res.date
                self.env['offre.contrat'].create(values)

            elif res.letter_type_id.name in ['Bon de commande']:
                values['date_demande'] = res.date
                self.env['bon.commande'].create(values)

        return res

    @api.onchange('immeuble_id', 'all_immeuble')
    def onchange_immeuble(self):
        prop_list = []
        if self.all_immeuble:
            for lot in self.immeuble_id.lot_ids:
                for prop in lot.proprio_id:
                    if prop.id not in prop_list:
                        prop_list.append(prop.id)
            self.propr_ids = prop_list
        else:
            self.propr_ids = []

    @api.onchange('propr_ids', 'fourn_ids', 'loc_ids')
    def onchange_partner(self, context=None):
        partner_address_ids = []
        partner_address_env = self.env['partner.address']

        for owner_id in self.propr_ids:
            partner_address_ids += partner_address_env.search([('add_parent_id_owner', '=', owner_id['id']),
                                                               ('is_letter', '=', True)])
        for supplier_id in self.fourn_ids:
            partner_address_ids += partner_address_env.search([('add_parent_id_supplier', '=', supplier_id['id']),
                                                               ('is_letter', '=', True)], context=context)
        for loaner_id in self.loc_ids:
            partner_address_ids += partner_address_env.search([('add_parent_id_loaner', '=', loaner_id['id']),
                                                               ('is_letter', '=', True)])

        self.partner_address_ids = [(6, 0, [partner_id.id for partner_id in partner_address_ids])]

        if len(self.fourn_ids) > 0:
            self.is_fax = True
        else:
            self.is_fax = False

    @api.one
    def send_email_lettre(self):
        mail = {}
        header = ''
        mail['mail_server_id'] = self.mail_server.id
        mail['email_from'] = self.env.user.email
        mail['reply_to'] = self.env.user.email

        if self.immeuble_id:
            header = header + 'Concerne ' + self.immeuble_id.name + '<br/>'
            header = header + self.immeuble_id.address_building + '<br/>'
            header = header + str(self.immeuble_id.zip_building) + ' ' + str(self.immeuble_id.city_building.name)

        footer = "<br/>L'&eacute;quipe SG IMMO<br/>"
        footer += "Rue Fran&ccedil;ois Vander Elst, 38/1<br/>"
        footer += "1950 Kraainem<br/>"
        footer +='<img src="https://lh6.googleusercontent.com/-7QA8bP7oscU/UUrXkQ1-rHI/AAAAAAAAAAk/WhbiGpLAUCQ/s270/Logo_SG%2520immo.JPG" width="96" height="61"/>'

        if self.ps:
            mail['body_html'] = header + '<br/><br/>' + self.begin_letter_id.name + '<br/>' + self.contenu + '<br/>Cordialement.<br/><br/>' + self.ps + '<br/>'+footer
        else:
            mail['body_html'] = header + '<br/><br/>' + self.begin_letter_id.name + '<br/>' + self.contenu + '<br/>Cordialement.<br/><br/>'+footer

        if self.immeuble_id:
            mail['subject'] = self.immeuble_id.name + '-' + self.sujet
        else:
            mail['subject'] = self.sujet

        attachment_ids = []
        for piece_jointe_id in self.piece_jointe_ids:
            attachment_ids.append((4, piece_jointe_id.attachement_id.id))

        mail['attachment_ids'] = attachment_ids

        for prop in self.propr_ids:
            if prop.email:
                mail['email_to'] = prop.email
                self.env['mail.mail'].create(mail)

        for fourn in self.fourn_ids:
            if fourn.email:
                mail['email_to'] = fourn.email
                self.env['mail.mail'].create(mail)

        for loc in self.loc_ids:
            if loc.email:
                mail['email_to'] = loc.email
                self.env['mail.mail'].create(mail)

        for div in self.divers_ids:
            if div.email:
                mail['email_to'] = div.email
                self.env['mail.mail'].create(mail)

        self.is_mail = True
        self.state = 'send'

    @api.onchange('letter_model_id')
    def onchange_letter(self):
        self.contenu = self.letter_model_id.text


class end_letter(models.Model):
    _name = 'letter.end'
    name = fields.Char('Fin de lettre', required=True)


class begin_letter(models.Model):
    _name = 'letter.begin'
    name = fields.Char('Debut de lettre', required=True)


class letter_type(models.Model):
    _name = 'letter.type'
    name = fields.Char('Type Letter', required=True)


class letter_model(models.Model):
    _name = 'letter.model'
    name = fields.Char('Model Letter', required=True)
    text = fields.Html('Text', required=True)


class letter_model_avis(models.Model):
    _name = 'letter.avis.model'
    name = fields.Char('Nom du modèle')
    text = fields.Html('Avis')