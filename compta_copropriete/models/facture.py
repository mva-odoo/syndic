# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Facture(models.Model):
    _name = 'syndic.compta.facture'

    name = fields.Char('Facture')
    payment_type = fields.Selection([('pret', 'Prêt'), ('cash', 'Cash')], 'Type de payement')
    ligne_ids = fields.One2many('syndic.compta.facture.ligne', 'facture_id', 'Ligne de Facture')
    payment_split_ids = fields.One2many('syndic.compta.facture.payment.split', 'facture_id', 'Facture')
    type = fields.Selection([('in', 'In'), ('out', 'Out')], 'Type')
    building_id = fields.Many2one('syndic.building', 'Immeuble')
    fournisseur_id = fields.Many2one('syndic.supplier', 'Fournisseur')
    exercice_id = fields.Many2one('syndic.compta.exercice', 'Exercice')

    def split_facture(self):
        # arrondie
        pass

    def facture_name(self):
        pass

    def compute_payment(self):
        pass


class FactureLigne(models.Model):
    _name = 'syndic.compta.facture.ligne'
    # _rec_name = 'product_id.name'

    amount = fields.Float('Montant unitaire')
    qty = fields.Integer('Qunatité')
    total_amount = fields.Float('Montant totale')
    facture_id = fields.Many2one('syndic.compta.facture', 'Facture')
    repartition_id = fields.Many2one('syndic.compta.repartition', 'Répartition')
    product_id = fields.Many2one('syndic.compta.product', 'Produit')
    is_amortissement = fields.Boolean('Amortir')

    @api.onchange('qty', 'amount')
    def onchange_amount(self):
        self.total_amount = self.qty*self.amount

    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            self.amount = self.product_id.amount

class FactureLigne(models.Model):
    _name = 'syndic.compta.facture.payment.split'

    amount = fields.Float('Montant')
    payment_ids = fields.One2many('syndic.compta.payment', 'payment_split_id', 'Payements')
    facture_id = fields.Many2one('syndic.compta.facture.facture', 'Facture')
