# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _


class Claim(models.Model):
    _name = 'syndic.claim'
    _inherit = ['mail.thread']
    _description = 'syndic.claim'
    _rec_name = 'subject'
    _order = 'create_date desc'

    def _default_statut(self):
        return self.env['claim.status'].search(
            [],
            order='sequence asc',
            limit=1
        ).id

    subject = fields.Char('Sujet', required=True)
    manager_id = fields.Many2one(
        'res.users',
        string='Gestionnaire de la plainte',
        domain=['!', ('groups_id.name', 'ilike', 'Syndic/Client')],
        default=lambda self: self.env.uid
    )
    partner_ids = fields.Many2many('res.partner', string='Contacts')
    claim_status_id = fields.Many2one(
        'claim.status',
        string='Status',
        tracking=True,
        default=_default_statut,
        group_expand='_read_group_stage_ids'
    )
    building_id = fields.Many2one('syndic.building', 'Immeuble')
    importance = fields.Selection([
        ('0', 'pas important'),
        ('1', 'important'),
        ('2', 'tres important'),
        ('3', 'ultra important')
    ], string='Importance')
    color = fields.Integer('Color')
    type_id = fields.Many2one('claim.type', 'Type')

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return self.env['claim.status'].search([])

    def add_follower_claim(self):
        self.ensure_one()
        self.message_subscribe(
                partner_ids=self.partner_ids.ids
        )

    def _get_creation_message(self):
        return 'Creation du ticket'

    @api.model
    def create(self, vals):
        res = super(Claim, self).create(vals)

        if res.manager_id.id != res.create_uid.id:
            body = """
Bonjour,

une tâche t'attends sur : <a href='https://sgimmo.be/web#id=%i&view_type=form&model=syndic.claim&menu_id=128&action=119'>Odoo</a>
""" % res.id

            res.message_subscribe(partner_ids=res.manager_id.partner_id.ids)
            res.message_post(body=_(body), partner_ids=res.manager_id.partner_id.ids)

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
