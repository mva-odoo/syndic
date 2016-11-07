# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Wizard_payment(models.TransientModel):
    _name = 'syndic.compta.wizard.payment'

    type_payement = fields.Selection([
        ('compte', 'Comtpe'),
        ('amortissement', 'Amortissemnt'),
        ('emprunt', 'Emprunt'),
    ])
    bank_account_id = fields.Many2one('syndic.compta.bank.account', 'Compte en banque')
    amortissement_year = fields.Integer("Année d'amortissement")

    @api.multi
    def payment(self):
        if self._context.get('active_id'):
            facture = self.env['syndic.compta.facture'].browse(self._context.get('active_id'))

            if self.type_payement == 'compte':
                self.env['syndic.compta.account'].create({
                    'account_id': facture.fournisseur_id.account_id.id,
                    'facture_id': facture.id,
                    'debit': facture.total_amount
                })

                self.env['syndic.compta.account'].create({
                    'account_id': self.bank_account_id.account_id.id,
                    'facture_id': facture.id,
                    'credit': facture.total_amount
                })
