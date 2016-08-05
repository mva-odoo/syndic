# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Facture(models.Model):
    _name = 'syndic.compta.facture'

    name = fields.Char('Facture')
    payment_type = fields.Selection([('pret', 'Prêt'), ('cash', 'Cash')], 'Type de payement')
    ligne_ids = fields.One2many('syndic.compta.facture.ligne', 'facture_id', 'Ligne de Facture')
    payment_ids = fields.One2many('syndic.compta.payment', 'facture_id', 'Payements')
    type = fields.Selection([('in', 'In'), ('out', 'Out')], 'Type')
    building_id = fields.Many2one('syndic.building', 'Immeuble')
    fournisseur_id = fields.Many2one('syndic.supplier', 'Fournisseur')

    def split_facture(self):
        # arrondie
        pass

    def facture_name(self):
        pass


class FactureLigne(models.Model):
    _name = 'syndic.compta.facture.ligne'
    # _rec_name = 'product_id.name'

    # product_id = fields.Many2one()
    amount = fields.Float('Montant unitaire')
    qty = fields.Integer('Qunatité')
    total_amount = fields.Integer('Montant totale')
    facture_id = fields.Many2one('syndic.compta.facture', 'Facture')
    repartition_id = fields.Many2one('syndic.compta.repartition', 'Répartition')
    product_id = fields.Many2one('syndic.compta.product', 'Produit')
    is_amortissement = fields.Boolean('Amortir')
