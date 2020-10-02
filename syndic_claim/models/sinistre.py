# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _


class ClaimRepair(models.Model):
    _name = 'syndic.claim.sinistre.repair'
    _description = 'syndic.claim.sinistre.repair'

    invoice_ids = fields.Many2many('account.move', string='Factures')
    is_repair = fields.Boolean('Reparé?')
    remboursement = fields.Char("remboursement de l'assurance")
    claim_id = fields.Many2one('syndic.claim.sinistre.repair', 'Reparation')
