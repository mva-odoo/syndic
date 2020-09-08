# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import date


class Claim(models.Model):
    _name = 'syndic.claim'
    _inherit = ['mail.thread']
    _description = 'syndic.claim'
    _rec_name = 'subject'
    _order = 'create_date desc'

    subject = fields.Char('Sujet', required=True)
    manager_id = fields.Many2one(
        'res.users',
        string='Gestionnaire de la plainte',
        domain=['!', ('groups_id.name', 'ilike', 'Syndic/Client')],
        default=lambda self: self.env.uid
    )
    partner_ids = fields.Many2many('res.partner', string='Contacts')
    claim_status_id = fields.Many2one('claim.status', string='Status', tracking=True)
    building_id = fields.Many2one('syndic.building', 'Immeuble')
    importance = fields.Selection([
        ('0', 'pas important'),
        ('1', 'important'),
        ('2', 'tres important'),
        ('3', 'ultra important')
    ], string='Importance')
    color = fields.Integer('Color', compute="_get_color")
    type_id = fields.Many2one('claim.type', 'Type')

    @api.depends('importance')
    def _get_color(self):
        for rec in self:
            rec.color = rec.importance

    def write(self, vals):
        res = super(Claim, self).write(vals)
        for rec in self:
            rec.message_subscribe(
                partner_ids=(rec.partner_ids | rec.manager_id.partner_id).ids
            )
        return res

    @api.model
    def create(self, vals):
        res = super(Claim, self).create(vals)
        res.message_subscribe(partner_ids=(res.partner_ids | res.manager_id.partner_id).ids)

        if res.manager_id.id != res.create_uid.id:
            body = """
Bonjour,

une tâche t'attends sur : <a href='https://sgimmo.be/web#id=%i&view_type=form&model=syndic.claim&menu_id=128&action=119'>Odoo</a>
""" % res.id

            self.env['mail.mail'].create({
                'mail_server_id':  self.env.user.server_mail_id.id or False,
                'email_from': self.env.user.email,
                'reply_to': self.env.user.email,
                'body_html': body,
                'subject': 'Une tâche t\'attends dans Odoo',
                'email_to': self.env['res.users'].browse(vals.get('manager_id')).email
            })

        return res


class ClaimStatus(models.Model):
    _name = 'claim.status'
    _description = 'claim.status'

    name = fields.Char('Status', required=True)
    sequence = fields.Integer('Status sequence')


class ClaimType(models.Model):
    _name = 'claim.type'
    _description = 'claim.type'

    name = fields.Char('Status', required=True)
