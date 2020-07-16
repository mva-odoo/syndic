# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import date


class OffreContrats(models.Model):
    _name = 'offre.contrat'
    _inherit = ['barcode.import']
    _description = 'offre.contrat'
    _order = 'date_envoi desc'

    _barcode_type = 'offre'

    code = fields.Char('Code', readonly=True)
    name = fields.Char('Type', required=True)
    fournisseur_id = fields.Many2one('res.partner', string='Nom du fournisseur', required=True)
    immeuble_id = fields.Many2one('syndic.building', string='Nom immeuble', required=True)
    demande = fields.Selection([('offre', 'Offre'), ('contrat', 'Contrat')], string='Demande')
    date_envoi = fields.Date('Date envoi', required=True)
    envoi_par = fields.Selection([
        ('recommende', 'Par recommandé'),
        ('courrier_simple', 'Par courrier simple'),
        ('email', 'Par Email'),
        ('fax', 'Par Fax')], string=u'Envoyé par')
    reception = fields.Boolean('Reception')
    date_reception = fields.Date('Date reception')
    transmition = fields.Boolean('Transmition')
    date_transmition = fields.Date('Date transmition')
    acceptation = fields.Boolean('Est Acceptate')
    accept = fields.Selection([
        ('accepte', 'Accepté'),
        ('non_accpet', 'Pas accepté')], 'Acceptation')
    date_acceptation = fields.Date('Date acceptation')
    is_bon_commande = fields.Boolean('Bon de commande fait', default=False)
    is_refused = fields.Boolean('Refuser', default=False)
    attachment_ids = fields.Many2many('ir.attachment', string='Offres')

    @api.onchange('reception')
    def onchange_reception(self):
        self.date_reception = date.today().strftime('%Y-%m-%d') if self.reception else False

    @api.onchange('transmition')
    def onchange_transmition(self):
        self.date_transmition = date.today().strftime('%Y-%m-%d') if self.transmition else False

    @api.onchange('acceptation')
    def onchange_acceptation(self):
        self.date_acceptation = date.today().strftime('%Y-%m-%d') if self.acceptation else False

    def transform_bon_commande(self):
        self.ensure_one()
        self.env['bon.commande'].create({
            'name': self.name,
            'immeuble_id': self.immeuble_id.id,
            'fournisseur_id': self.fournisseur_id.id,
            'date_demande': self.date_acceptation,
        })
        self.is_bon_commande = True
