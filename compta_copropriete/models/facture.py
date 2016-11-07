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
    total_amount = fields.Float('Total amount', compute='_get_total_amount')
    account_ids = fields.One2many('syndic.compta.account', 'facture_id', 'Comptes')

    @api.model
    def create(self, vals):
        building_id = self.env['syndic.building'].browse(vals['building_id'])
        sequence = self.env['ir.sequence'].next_by_code('Facture - %s' % building_id.name)
        if not sequence:
            raise exceptions.ValidationError('Il n\'y pas de sequence pour cet immeuble. Solution: appeler super michou')
        vals['name'] = sequence
        return super(Facture, self).create(vals)

    @api.multi
    def _get_total_amount(self):
        for facture in self:
            amount = 0.00
            for ligne in facture.ligne_ids:
                amount += ligne.total_amount
            self.total_amount = amount

    @api.multi
    def validate_facture(self):
        for facture in self:
            for ligne in facture.ligne_ids:
                total_amount = 0.00
                for repartition_ligne in ligne.repartition_id.repart_detail_ids:

                    split_value = (ligne.total_amount/ligne.repartition_id.percentage_lot) * repartition_ligne.value
                    self.env['syndic.compta.facture.payment.split'].create({
                        'amount': split_value,
                        'facture_id': facture.id,
                        'lot_id': repartition_ligne.id,
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
                self.env['syndic.compta.account'].create({
                    'account_id': ligne.product_id.account_id.id,
                    'debit': ligne.total_amount,
                    'facture_id': facture.id,
                })

                self.env['syndic.compta.account'].create({
                    'account_id': facture.fournisseur_id.account_id.id,
                    'credit': ligne.total_amount,
                    'facture_id': facture.id,
                })

            self.state = 'validate'

    @api.multi
    def pay_facture(self):
        return {
            'name': 'Payement',
            'type': 'ir.actions.act_window',
            'src_model': "syndic.compta.facture",
            'res_model': 'syndic.compta.wizard.payment',
            'view_mode': 'form',
            'target': 'new',
        }


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
    _rec_name = 'amount'

    amount = fields.Float('Montant')
    payment_ids = fields.One2many('syndic.compta.payment', 'payment_split_id', 'Payements')
    facture_id = fields.Many2one('syndic.compta.facture.facture', 'Facture')
    lot_id = fields.Many2one('syndic.lot', 'Lot')
