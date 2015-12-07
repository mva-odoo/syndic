# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Facture(models.Model):
    _inherit = 'syndic.facturation'

    @api.depends('immeuble_id')
    @api.one
    def _compute_exercice(self):
        if not self.state == 'report':
            self.exercice_id = self.immeuble_id.current_exercice_id
        else:
            self.exercice_id = False

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

        if total >= 100.0:
            self.write({'state': 'close'})

    invoice_date = fields.Date('Date de création', default=lambda *a: fields.date.today())
    state = fields.Selection([('report', 'Report'), ('draft', 'Brouillon'), ('validate', 'Validé'), ('close', 'Payé')],
                             'Etat', default='draft')
    facture_detail_ids = fields.One2many('syndic.facture.detail', 'facture_id', 'Detail de facture')
    bilan_ids = fields.One2many('syndic.bilan.ligne', 'facture_id', 'Lignes du bilan')
    exercice_id = fields.Many2one('syndic.exercice', 'Exercice', compute=_compute_exercice, store=True)
    proprietaire_ids = fields.Many2many('syndic.owner', string='Proprietaires')
    pay_percentage = fields.Float('Pourcentage de payement', compute=_compute_percentage)
    communication = fields.Char('Communication virement')

    @api.one
    def validate_facture(self):
        if self.state != 'validate':
            for line in self.line_ids:
                check_amount = 0.00
                if line.repartition_lot_id:
                    for repartition_line in line.repartition_lot_id.repart_detail_ids:
                        amount = line.prix * (repartition_line.value/1000)
                        proprio_ids = False
                        if repartition_line.lot_id.proprio_id:
                            proprio_ids = [prop_id.id for prop_id in repartition_line.lot_id.proprio_id]
                        self.env['syndic.facture.detail'].create({
                            'facture_id': self.id,
                            'facture_line_id': line.id,
                            'amount': amount,
                            'lot_id': repartition_line.lot_id.id,
                            'proprietaire_ids': [(6, 0, proprio_ids)],
                            'product_id': line.type_id.id,
                            'fournisseur_id': line.fournisseur_id.id,
                        })

                        check_amount += amount
                else:
                    self.env['syndic.facture.detail'].create({
                            'facture_id': self.id,
                            'facture_line_id': line.id,
                            'amount': line.prix,
                            'product_id': line.type_id.id,
                            'fournisseur_id': line.fournisseur_id.id,
                        })
                if self.state == 'draft':
                    self.env['syndic.bilan.ligne'].create({
                            'name': line.type_id.name,
                            'facture_id': self.id,
                            'account_id': line.type_id.receive_compte_id.id,
                            'debit': line.prix,
                            'exercice_id': line.facture_id.exercice_id.id,
                        })

                    self.env['syndic.bilan.ligne'].create({
                            'name': line.type_id.name,
                            'facture_id': self.id,
                            'account_id': line.fournisseur_id.account_id.id or line.type_id.accompte_fond_id.id,
                            'credit': line.prix,
                            'exercice_id': line.facture_id.exercice_id.id,
                        })
                    if check_amount != line.prix and line.repartition_lot_id:
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
        new_id.name = '%s/%i' % (building.name, new_id)
        return new_id

    @api.one
    def pay_all_facture(self):
        for detail_id in self.facture_detail_ids:
            if not detail_id.is_paid:
                detail_id.pay_all()
        self.state = 'close'


class FactureLigne(models.Model):
    _inherit = 'syndic.facturation.line'

    @api.onchange('name', 'prix', 'invoice_line_date', 'type_id')
    def _compute_immeuble(self):
        self.immeuble_id = self.facture_id.immeuble_id.id

    invoice_line_date = fields.Date('Date d\'echéhance')
    fournisseur_id = fields.Many2one('syndic.supplier', 'Fournisseur')
    repartition_lot_id = fields.Many2one('syndic.repartition.lot', 'Répartition des Lots')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')


class FactureDetail(models.Model):
    _name = 'syndic.facture.detail'
    _rec_name = 'facture_id'

    facture_id = fields.Many2one('syndic.facturation', 'origine facture', required=True)
    exercice_id = fields.Many2one('syndic.exercice', related='facture_id.exercice_id', store=True, string='Exercice')
    facture_line_id = fields.Many2one('syndic.facturation.line', 'origine ligne', required=True)
    amount = fields.Float('Montant', required=True)
    lot_id = fields.Many2one('syndic.lot', 'Lot')
    product_id = fields.Many2one('syndic.facturation.type', 'Type')
    proprietaire_ids = fields.Many2many('syndic.owner', string='Propriétaire')
    fournisseur_id = fields.Many2one('syndic.supplier', 'Fournisseur')
    is_paid = fields.Boolean('Payé', readonly=True)
    is_amortissement = fields.Boolean('Amorti', readonly=True)
    is_report = fields.Boolean('Report')
    amortissement_ids = fields.One2many('syndic.compta.amortissement', 'facture_detail_id', 'Amorrtissements')
    already_pay = fields.Float('Deja payé')
    report_facture_id = fields.Many2one('syndic.facturation', 'Facture reportée')
    is_amortissable = fields.Boolean('est amortissable', related='product_id.is_amortissable')

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
    @api.one
    def report_pay(self):
        ligne = self.env['syndic.facturation.ligne'].create({
            'name': self.facture_line_id.name,
            'amount': self.amount - self.already_pay,
            'immeuble_id': self.facture_line_id.immeuble_id.id,
            'product_id': self.facture_line_id.product_id.id,
            'fournisseur_id': self.facture_line_id.fournisseur_id.id,
            'invoice_line_date': self.facture_line_id.invoice_line_date,
        })

        facture_id = self.env['syndic.facturation'].create({
            'name': 'report',
            'immeuble_id': self.facture_line_id.immeuble_id.id,
            'state': 'report',
            'line_ids': [(6, 0, [ligne.id])]
        })

        self.write({'report_facture_id': facture_id.id, 'is_report': True})

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

    @api.multi
    def split_pay_wizard(self):
        return {
            'name': 'Split montant',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'syndic.compta.split.pay.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': self._context,
        }


class SplitPayWizard(models.Model):
    _name = 'syndic.compta.split.pay.wizard'

    amount = fields.Float('Montant')


    @api.one
    def split_pay(self):
        detail = self.env['syndic.facture.detail'].browse(self._context['active_id'])
        new_amount = detail.already_pay+self.amount
        if new_amount > detail.amount:
            raise exceptions.Warning('Vous essayez de payer plus que vous devez')
        elif new_amount == detail.amount:
            detail.write({'is_paid': True})

        detail.write({'already_pay': new_amount})

        prop_name = ''
        proprio_name = [proprio.name for proprio in detail.proprietaire_ids]
        if proprio_name:
            prop_name = ', '.join(proprio_name)
        self.env['syndic.bilan.ligne'].create({
            'name': 'payement '+detail.product_id.name+' par '+prop_name,
            'facture_id': detail.facture_id.id,
            'account_id': detail.product_id.payable_compte_id.id,
            'exercice_id': detail.facture_id.exercice_id.id,
            'credit': new_amount,
            'immeuble_id': detail.facture_id.immeuble_id.id,
        })
        self.env['syndic.bilan.ligne'].create({
            'name': 'payement '+detail.product_id.name,
            'facture_id': detail.facture_id.id,
            'account_id': detail.fournisseur_id.account_id.id or detail.product_id.etablissement_fond.id,
            'exercice_id': detail.facture_id.exercice_id.id,
            'debit': new_amount,
            'immeuble_id': detail.facture_id.immeuble_id.id,
        })