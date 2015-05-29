# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
import datetime

class Facture(models.Model):
    _name = 'syndic.facture'

    @api.depends('immeuble_id')
    @api.one
    def _compute_exercice(self):
        self.exercice_id = self.immeuble_id.current_exercice_id

    @api.depends('facture_detail_ids')
    @api.one
    def _compute_percentage(self):
        payed = []
        total = 0.00
        for detail_id in self.facture_detail_ids:
            if detail_id.is_paid:
                payed.append(detail_id.id)
        if self.facture_detail_ids:
            total = (len(payed)/float(len(self.facture_detail_ids)))*100

        self.pay_percentage = total

    name = fields.Char('Facture numeros')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble', required=True)
    invoice_date = fields.Date('Date de création', default=lambda *a: fields.date.today())
    facture_line_ids = fields.One2many('syndic.facture.ligne', 'facture_id', 'Ligne de facture')
    state = fields.Selection([('draft', 'Brouillon'), ('validate', 'Validé'), ('close', 'Payé')],
                             'Etat', default='draft')
    facture_detail_ids = fields.One2many('syndic.facture.detail', 'facture_id', 'Detail de facture')
    bilan_ids = fields.One2many('syndic.bilan.ligne', 'facture_id', 'Lignes du bilan')
    exercice_id = fields.Many2one('syndic.exercice', 'Exercice', compute=_compute_exercice, required=True)
    proprietaire_ids = fields.Many2many('syndic.owner', string='Proprietaires')
    pay_percentage = fields.Float('Pourcentage de payement', compute=_compute_percentage)

    @api.one
    def validate_facture(self):
        if self.state != 'validate':
            for line in self.facture_line_ids:
                check_amount = 0.00
                if line.repartition_lot_id:
                    for repartition_line in line.repartition_lot_id.repart_detail_ids:
                        amount = line.amount * (repartition_line.value/1000)
                        proprio_ids = False
                        if repartition_line.lot_id.proprio_id:
                            proprio_ids = [prop_id.id for prop_id in repartition_line.lot_id.proprio_id]
                        self.env['syndic.facture.detail'].create({
                            'facture_id': self.id,
                            'facture_line_id': line.id,
                            'amount': amount,
                            'lot_id': repartition_line.lot_id.id,
                            'proprietaire_ids': [(6, 0, proprio_ids)],
                            'product_id': line.product_id.id,
                            'fournisseur_id': line.fournisseur_id.id,
                        })

                        check_amount += amount
                else:
                    self.env['syndic.facture.detail'].create({
                            'facture_id': self.id,
                            'facture_line_id': line.id,
                            'amount': line.amount,
                            'product_id': line.product_id.id,
                            'fournisseur_id': line.fournisseur_id.id,
                        })

                self.env['syndic.bilan.ligne'].create({
                        'name': line.product_id.name,
                        'facture_id': self.id,
                        'account_id': line.product_id.receive_compte_id.id,
                        'debit': line.amount,
                        'exercice_id': line.facture_id.exercice_id.id,
                    })

                self.env['syndic.bilan.ligne'].create({
                        'name': line.product_id.name,
                        'facture_id': self.id,
                        'account_id': line.fournisseur_id.account_id.id or line.product_id.accompte_fond_id.id,
                        'credit': line.amount,
                        'exercice_id': line.facture_id.exercice_id.id,
                    })
                if check_amount != line.amount and line.repartition_lot_id:
                    raise exceptions.Warning("La totalité de la somme n'a pas été facturé. "
                                             "Vérifié la répartition des quotités")

            self.state = 'validate'

    @api.one
    def reset_draft(self):
        self.facture_detail_ids.unlink()
        self.bilan_ids.unlink()
        self.state = 'draft'

    @api.model
    def create(self, vals):
        new_id = super(Facture, self).create(vals)
        building = self.env['syndic.building'].search([('id', '=', vals['immeuble_id'])])
        new_id.name = '%s/%i' %(building.name, new_id)
        return new_id

    @api.one
    def pay_all_facture(self):
        for detail_id in self.facture_detail_ids:
            if not detail_id.is_paid:
                detail_id.pay_all()
        self.state = 'close'

class FactureLigne(models.Model):
    _name = 'syndic.facture.ligne'

    @api.onchange('name', 'amount', 'invoice_line_date', 'prodcut_id')
    def _compute_immeuble(self):
        self.immeuble_id = self.facture_id.immeuble_id.id

    name = fields.Char('Description', required=True)
    amount = fields.Float('Montant', required=True)
    invoice_line_date = fields.Date('Date d\'echéhance')
    fournisseur_id = fields.Many2one('syndic.supplier', 'Fournisseur')
    product_id = fields.Many2one('syndic.product', 'Produit', required=True)
    repartition_lot_id = fields.Many2one('syndic.repartition.lot', 'Répartition des Lots')
    facture_id = fields.Many2one('syndic.facture', 'Facture')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')


class FactureDetail(models.Model):
    _name = 'syndic.facture.detail'
    _rec_name ='facture_id'

    facture_id = fields.Many2one('syndic.facture', 'origine facture', required=True)
    facture_line_id = fields.Many2one('syndic.facture.ligne', 'origine ligne', required=True)
    amount = fields.Float('Montant', required=True)
    lot_id = fields.Many2one('syndic.lot', 'Lot')
    product_id = fields.Many2one('syndic.product', 'Produit')
    proprietaire_ids = fields.Many2many('syndic.owner', string='Propriétaire')
    fournisseur_id = fields.Many2one('syndic.supplier', 'Fournisseur')
    is_paid = fields.Boolean('Payé', readonly=True)
    is_amortissement = fields.Boolean('Amorti', readonly=True)
    amortissement_ids = fields.One2many('syndic.compta.amortissement', 'facture_detail_id', 'Amorrtissements')

    @api.one
    def pay_all(self):
        prop_name = ''
        proprio_name = [proprio.name for proprio in self.proprietaire_ids]
        if proprio_name:
            prop_name = ', '.join(proprio_name)
        self.env['syndic.bilan.ligne'].create({
            'name': 'payement '+self.product_id.name+' par '+prop_name,
            'facture_id': self.facture_id.id,
            'account_id': self.product_id.payable_compte_id.id,
            'exercice_id': self.facture_id.exercice_id.id,
            'credit': self.amount,
            'immeuble_id': self.facture_id.immeuble_id.id,
        })
        self.env['syndic.bilan.ligne'].create({
            'name': 'payement '+self.product_id.name,
            'facture_id': self.facture_id.id,
            'account_id': self.fournisseur_id.account_id.id or self.product_id.etablissement_fond.id,
            'exercice_id': self.facture_id.exercice_id.id,
            'debit': self.amount,
            'immeuble_id': self.facture_id.immeuble_id.id,
        })

        self.is_paid = True

    @api.multi
    def amortissement_wizard(self):
        return {
            'name': 'Amortissement',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'syndic.amortissement.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': self._context,
        }