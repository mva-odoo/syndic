# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
import datetime


class SyndicComptaSetting(models.Model):
    _name = 'syndic.compta.setting'

    roulement_product_id = fields.Many2one('syndic.product', 'Produit d ouverture (roulement)')
    reserve_product_id = fields.Many2one('syndic.product', 'Produit d ouverture (resrve)')
    compte_rapporter = fields.Many2one('syndic.pcmn', 'Compte à reporter')
    report_reserve_compte = fields.Many2one('syndic.pcmn', 'Compte de fond de reserve à reporter')
    report_roulement_compte = fields.Many2one('syndic.pcmn', 'Compte de fond de roulement à reporter')
    open_report_reserve_compte = fields.Many2one('syndic.product', 'Produit de fond de reserve à reporter pour reouverture')
    open_report_roulement_compte = fields.Many2one('syndic.product', 'Produit de fond de roulement à reporter pour reouverture')
    fournisseur_compte = fields.Many2one('syndic.pcmn', 'Compte fournisseur')


class SyndicBuilding(models.Model):
    _inherit = 'syndic.building'

    def _default_prod_roulement(self):
        settings = self.env['syndic.compta.setting'].search([])
        if len(settings) > 0:
            return settings.roulement_product_id.id
        return settings.roulement_product_id

    def _default_prod_reserve(self):
        settings = self.env['syndic.compta.setting'].search([])
        if len(settings) > 0:
            return settings.reserve_product_id.id
        return settings.roulement_product_id

    def _default_compte_rapporter(self):
        settings = self.env['syndic.compta.setting'].search([])
        if len(settings) > 0:
            return settings.compte_rapporter.id
        return settings.roulement_product_id

    def _default_report_reserve_compte(self):
        settings = self.env['syndic.compta.setting'].search([])
        if len(settings) > 0:
            return settings.report_reserve_compte.id
        return settings.roulement_product_id

    def _default_report_roulement_compte(self):
        settings = self.env['syndic.compta.setting'].search([])
        if len(settings) > 0:
            return settings.report_roulement_compte.id
        return settings.roulement_product_id

    def _default_open_report_reserve_compte(self):
        settings = self.env['syndic.compta.setting'].search([])
        if len(settings) > 0:
            return settings.open_report_reserve_compte.id
        return settings.roulement_product_id

    roulement_product_id = fields.Many2one('syndic.product', 'Produit d ouverture (roulement)',
                                           default=_default_prod_roulement)
    reserve_product_id = fields.Many2one('syndic.product', 'Produit d ouverture (resrve)',
                                         default=_default_prod_reserve)
    compte_rapporter = fields.Many2one('syndic.pcmn', 'Compte à reporter',
                                       default=_default_compte_rapporter)
    report_reserve_compte = fields.Many2one('syndic.pcmn', 'Compte de fond de reserve à reporter',
                                            default=_default_report_reserve_compte)
    report_roulement_compte = fields.Many2one('syndic.pcmn', 'Compte de fond de roulement à reporter',
                                              default=_default_report_roulement_compte)
    open_report_reserve_compte = fields.Many2one('syndic.product',
                                                 'Produit de fond de reserve à reporter pour reouverture',
                                                 default=_default_open_report_reserve_compte)
    open_report_roulement_compte = fields.Many2one('syndic.product',
                                                   'Produit de fond de roulement à reporter pour reouverture',
                                                   default=_default_open_report_reserve_compte)
    current_exercice_id = fields.Many2one('syndic.exercice', 'Exercice courant')
    detail_ids = fields.Many2many('syndic.bilan.ligne', string='Lignes comptable')


class Fournisseur(models.Model):
    _inherit = 'syndic.supplier'

    def _default_account_id(self):
        settings = self.env['syndic.compta.setting'].search([])
        if len(settings) > 0:
            return settings.fournisseur_compte.id
        return settings.fournisseur_compte

    account_id = fields.Many2one('syndic.pcmn', 'Compte Fournisseur', default=_default_account_id)


class SyndicLot(models.Model):
    _inherit = 'syndic.lot'

    line_facture_ids = fields.One2many('syndic.facture.detail', 'lot_id', string="Lignes de facture")
