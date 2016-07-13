# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
import datetime


class SyndicAmortissementWizard(models.TransientModel):
    _name = 'syndic.amortissement.wizard'

    def _default_product(self):
        return self.env['syndic.facture.detail'].browse(self._context.get('active_id')).product_id

    def _default_amount(self):
        return self.env['syndic.facture.detail'].browse(self._context.get('active_id')).amount

    @api.depends('duration')
    @api.one
    def _compute_split_amount(self):
        if self.duration > 0:
            self.split_amount = self.env['syndic.facture.detail'].browse(
                self._context.get('active_id')).amount / self.duration
        else:
            self.split_amount = 0.00

    product_id = fields.Many2one('syndic.facturation.type', 'Produit', default=_default_product)
    amount = fields.Float('Montant', default=_default_amount)
    duration = fields.Integer('Durée')
    split_amount = fields.Float('Montant Divisé', compute=_compute_split_amount)
    debit_account_id = fields.Many2one('syndic.pcmn', 'Compte de Debis pour l\'amortissement')
    credit_account_id = fields.Many2one('syndic.pcmn', 'Compte de Credit pour l\'amortissement')

    @api.one
    def amortir(self):
        detail = self.env['syndic.facture.detail'].browse(self._context.get('active_id'))
        self.env['syndic.compta.amortissement'].create({
            'product_id': self.product_id.id,
            'amount': self.split_amount,
            'number': self.duration,
            'immeuble_id': detail.facture_id.immeuble_id.id,
            'facture_detail_id': detail.id,
            'debit_account_id': self.debit_account_id.id,
            'credit_account_id': self.credit_account_id.id,
            'stay_pay': self.amount,
            'counter': self.duration,
        })
        detail.is_amortissement = True


class ComptaAmortissement(models.Model):
    _name = 'syndic.compta.amortissement'
    _rec_name = 'product_id'

    product_id = fields.Many2one('syndic.facturation.type', 'Produit')
    active = fields.Boolean('Actif', default=True)
    amount = fields.Float('Montant')
    number = fields.Integer('Numeros de l\'accompte')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')
    facture_detail_id = fields.Many2one('syndic.facture.detail', 'Detail de facture')
    debit_account_id = fields.Many2one('syndic.pcmn', 'Compte de Debis pour l\'amortissement')
    credit_account_id = fields.Many2one('syndic.pcmn', 'Compte de Credit pour l\'amortissement')
    stay_pay = fields.Float('Reste à payer')
    counter = fields.Integer('Compteur')
