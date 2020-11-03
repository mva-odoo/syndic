# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.addons.syndic_tools.syndic_tools import SyndicTools

from jinja2 import Template


class PieceJointe(models.Model):
    _inherit = 'ir.attachment'

    letter_id = fields.Many2one('letter.letter', string='Lettre')


class CreateLetter(models.Model):
    _name = 'letter.letter'
    _description = 'letter.letter'
    _rec_name = 'sujet'
    _order = 'date desc'

    name = fields.Char('ID de la lettre', readonly=True)
    sujet = fields.Char('Sujet', required=True)
    immeuble_id = fields.Many2one('syndic.building', string='Immeuble')
    all_immeuble = fields.Boolean('Immeuble entier')

    old_ids = fields.Many2many('res.partner', 'letter_old_rel', string=u'Ancien Propriétaire')

    partner_ids = fields.Many2many('res.partner', 'letter_partner_rel', string="To")
    from_id = fields.Many2one(
        'res.users',
        string="From",
        default=lambda s: s.env.user,
        domain="[('groups_id.name','in',['Syndic/Employe','Syndic/Manager'])]"
    )

    end_letter_id = fields.Many2one('letter.end', 'Fin de lettre', required=True)
    begin_letter_id = fields.Many2one('letter.begin', u'Début de lettre', required=True)
    letter_type_id = fields.Many2one('letter.type', 'Type de lettre', required=True)
    letter_model_id = fields.Many2one('letter.model', u'Modèle de lettre')
    contenu = fields.Html('contenu', required=True)
    ps = fields.Text('PS')
    save_letter = fields.Boolean(u'Sauver la lettre comme modèle')
    name_template = fields.Char(u'Nom du modèle de lettre')
    is_mail = fields.Boolean('Envoi par email')
    is_fax = fields.Boolean('Envoi par fax')
    attachment_ids = fields.Many2many('ir.attachment', 'letter_letter_ir_attachment_rel', string='Piece Jointe')
    create_date = fields.Datetime(u'Date de création')
    date = fields.Date(u'Date de la lettre', default=lambda *a: fields.date.today(), copy=False)
    date_fr = fields.Char(string='Date', compute='_compute_date', store=True)
    partner_address_ids = fields.Many2many(
        'res.partner',
        String="Personne Jointe",
        compute='_get_other_address', store=True
    )
    state = fields.Selection([('not_send', 'Pas envoyé'), ('send', 'Envoyé')], string='State', default='not_send')
    mail_server = fields.Many2one('ir.mail_server', 'Serveur email')

    email_ids = fields.Many2many('mail.mail', compute='_get_email_letter', string='Emails')

    def _get_email_letter(self):
        for letter in self:
            letter.email_ids = self.env['mail.mail'].search([('model', '=', 'letter.letter'), ('res_id', '=', letter.id)])

    @api.depends('date')
    def _compute_date(self):
        for letter in self:
            letter.date_fr = SyndicTools().french_date(letter.date) if letter.date else ''

    def _get_jinja_template(self, contenu, vals):
        return Template(contenu).render(**vals)

    @api.model
    def create(self, vals):
        res = super(CreateLetter, self).create(vals)

        # create letter template
        if res.save_letter:
            res.env['letter.model'].create({'name': res.name_template, 'text': res.contenu})

        for supplier_id in res.partner_ids.filtered(lambda s: s.supplier):
            values = {
                'name': res.sujet,
                'fournisseur_id': supplier_id.id,
                'immeuble_id': res.immeuble_id.id,
            }

            if res.letter_type_id.name in ['Demande de devis', 'Demande d\'offre', 'Demande de contrat']:
                values['date_envoi'] = res.date
                self.env['offre.contrat'].create(values)

            elif res.letter_type_id.name in ['Bon de commande']:
                values['date_demande'] = res.date
                self.env['bon.commande'].create(values)
        return res

    @api.onchange('is_mail')
    def onchange_server(self):
        self.mail_server = self.env.user.server_mail_id.id if self.is_mail else False

    @api.onchange('immeuble_id', 'all_immeuble')
    def onchange_immeuble(self):
        self.partner_ids = self.immeuble_id.mapped('lot_ids.owner_id') if self.all_immeuble else False

    @api.onchange('partner_ids')
    def onchange_partner(self):
        self.partner_ids |= self.partner_ids.child_ids.filtered(lambda s: s.is_letter)

    def send_email_lettre(self):
        self.ensure_one()
        header = ''

        mail = {
            'model': 'letter.letter',
            'res_id': self.id,
            'mail_server_id': self.from_id.server_mail_id.id if self.from_id and self.from_id.server_mail_id else self.env.user.server_mail_id or False,
            'email_from': self.from_id.email if self.from_id else '',
            'reply_to': self.from_id.email if self.from_id else '',
            'attachment_ids': [(6, 0, self.attachment_ids.ids)],
            'subject': self.immeuble_id.name + '-' + self.sujet if self.immeuble_id else self.sujet,
        }

        if self.immeuble_id:
            header = "Concerne %s<br/>%s<br/>%s %s<br/><br/>" % (self.immeuble_id.name,
                                                                 self.immeuble_id.street,
                                                                 str(self.immeuble_id.zip),
                                                                 str(self.immeuble_id.city_id.name))

        body = "%s<br/>%s<br/>Cordialement.<br/><br/>" % (self.begin_letter_id.name, self.contenu)

        footer = """<br/>L'&eacute;quipe SG IMMO<br/>
Rue Fran&ccedil;ois Vander Elst, 38/1<br/>
1950 Kraainem<br/>
'<img src="https://lh6.googleusercontent.com/-7QA8bP7oscU/UUrXkQ1-rHI/AAAAAAAAAAk/WhbiGpLAUCQ/s270/Logo_SG%2520immo.JPG"
width="96" height="61"/>'"""

        mail['body_html'] = header + body + self.ps + '<br/>'+footer if self.ps else header + body + footer

        for prop in self.partner_ids.filtered(lambda s: s.email):
            mail['email_to'] = prop.email
            self.env['mail.mail'].create(mail)

        self.write({
            'is_mail': True,
            'state': 'send',
        })

    @api.onchange('letter_model_id')
    def onchange_letter(self):
        self.contenu = self.letter_model_id.text


class EndLetter(models.Model):
    _name = 'letter.end'
    _description = 'letter.end'

    name = fields.Char('Fin de lettre', required=True)


class BeginLetter(models.Model):
    _name = 'letter.begin'
    _description = 'letter.begin'

    name = fields.Char('Debut de lettre', required=True)


class LetterType(models.Model):
    _name = 'letter.type'
    _description = 'letter.type'

    name = fields.Char('Type Letter', required=True)


class LetterModel(models.Model):
    _name = 'letter.model'
    _description = 'letter.model'

    name = fields.Char('Model Letter', required=True)
    text = fields.Html('Text', required=True)
