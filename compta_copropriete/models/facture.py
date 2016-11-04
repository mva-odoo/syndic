# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Facture(models.Model):
    _name = 'syndic.compta.facture'

    name = fields.Char('Facture')
    ligne_ids = fields.One2many('syndic.compta.facture.ligne', 'facture_id', 'Ligne de Facture')
    payment_split_ids = fields.One2many('syndic.compta.facture.payment.split', 'facture_id', 'Facture')
    type = fields.Selection([('in', 'In'), ('out', 'Out')], 'Type')
    building_id = fields.Many2one('syndic.building', 'Immeuble', required=True)
    fournisseur_id = fields.Many2one('syndic.supplier', 'Fournisseur', required=True)
    state = fields.Selection([('Draft', 'Brouillon'), ('validate', 'Validé')])
    total_amount = fields.Float('Total amount')

    @api.model
    def create(self, vals):
        building_id = self.env['syndic.building'].browse(vals['building_id'])
        sequence = self.env['ir.sequence'].next_by_code('Facture - %s' % building_id.name)
        if not sequence:
            raise exceptions.ValidationError('Il n\'y pas de sequence pour cet immeuble. Solution: appeler super michou')
        vals['name'] = self.env['ir.sequence'].next_by_code('Facture - %s' % building_id.name)
        return super(Facture, self).create(vals)

    @api.multi
    def validate_facture(self):
        for facture in self:
            for ligne in facture.ligne_ids:
                total_amount = 0.00
                for repartition_ligne in ligne.repartition_id.repart_detail_ids:
                    split_value = (ligne.total_amount/repartition_ligne.value) * ligne.repartition_id.percentage_lot
                    self.env['syndic.compta.facture.payment.split'].create({
                        'amount': split_value,
                        'facture_id': facture.id,
                    })
                    total_amount += split_value

                # Arrondi
                arround = ligne.total_amount - total_amount
                if arround == 0.00 or arround != ligne.total_amount:
                    self.env['syndic.compta.facture.payment.split'].create({
                        'amount': arround,
                        'facture_id': self.id,
                    })
                # ecriture comptable
                ligne.product_id.account_id
                ligne.total_amount

                facture.fournisseur_id.account_id

            self.state = 'validate'

    @api.multi
    def pay_facture(self):
        for facture in self:
            for ligne in facture.ligne_ids:
                # create account lign
                pass


class FactureLigne(models.Model):
    _name = 'syndic.compta.facture.ligne'
    # _rec_name = 'product_id.name'

    amount = fields.Float('Montant unitaire', required=True)
    qty = fields.Integer('Quantité', default=1, required=True)
    total_amount = fields.Float('Montant totale')
    facture_id = fields.Many2one('syndic.compta.facture', 'Facture')
    repartition_id = fields.Many2one('syndic.compta.repartition', 'Répartition')
    product_id = fields.Many2one('syndic.compta.product', 'Produit', required=True)

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
