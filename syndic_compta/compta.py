# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
import datetime

class Facture(models.Model):
    _name = 'syndic.facture'
    name = fields.Char('Facture numeros')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble', required=True)
    invoice_date = fields.Date('Date de facture')
    facture_line_ids = fields.One2many('syndic.facture.ligne', 'facture_id', 'Ligne de facture')
    state = fields.Selection([('draft', 'Brouillon'), ('validate', 'Validé'), ('close', 'Fermé')],
                             'Etat', default='draft')
    facture_detail_ids = fields.One2many('syndic.facture.detail', 'facture_id', 'Detail de facture')
    bilan_ids = fields.One2many('syndic.bilan.ligne', 'facture_id', 'Lignes du bilan')
    exercice_id = fields.Many2one('syndic.exercice', 'Exercice')

    @api.one
    def validate_facture(self):
        if self.state != 'validate':
            for line in self.facture_line_ids:
                check_amount = 0.00

                for repartition_line in line.repartition_lot_id.repart_detail_ids:
                    amount = line.amount * (repartition_line.value/1000)
                    proprio_ids = False
                    if repartition_line.lot_id.proprio_id:
                        proprio_ids = [proprio_id.id for proprio_id in repartition_line.lot_id.proprio_id]
                    self.env['syndic.facture.detail'].create({
                        'facture_id': self.id,
                        'facture_line_id': line.id,
                        'amount': amount,
                        'lot_id': repartition_line.lot_id.id,
                        'proprietaire_ids': proprio_ids,
                        'product_id': line.product_id.id,
                        'fournisseur_id': line.fournisseur_id.id,
                    })

                    check_amount += amount

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
                if check_amount != line.amount:
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


class FactureLigne(models.Model):
    _name = 'syndic.facture.ligne'

    name = fields.Char('Description', required=True)
    amount = fields.Float('Montant', required=True)
    invoice_line_date = fields.Date('Date d\'echéhance', required=True)
    fournisseur_id = fields.Many2one('syndic.supplier', 'Fournisseur')
    product_id = fields.Many2one('syndic.product', 'Produit', required=True)
    repartition_lot_id = fields.Many2one('syndic.repartition.lot', 'Répartition des Lots', required=True)
    facture_id = fields.Many2one('syndic.facture', 'Facture')


class FactureDetail(models.Model):
    _name = 'syndic.facture.detail'
    facture_id = fields.Many2one('syndic.facture', 'origine facture', required=True)
    facture_line_id = fields.Many2one('syndic.facture.ligne', 'origine ligne', required=True)
    amount = fields.Float('Montant', required=True)
    lot_id = fields.Many2one('syndic.lot', 'Lot')
    product_id = fields.Many2one('syndic.product', 'Produit')
    proprietaire_ids = fields.Many2many('syndic.owner', string='Propriétaire')
    fournisseur_id = fields.Many2one('syndic.supplier', 'Fournisseur')
    is_paid =fields.Boolean('Payé', readonly=True)

    @api.one
    def pay_all(self):
        self.env['syndic.bilan.ligne'].create({
            'name': 'payement '+self.product_id.name+' par ',
            'facture_id': self.facture_id.id,
            'account_id': self.product_id.payable_compte_id.id,
            'exercice_id': self.facture_id.exercice_id.id,
            'credit': self.amount,
        })
        self.env['syndic.bilan.ligne'].create({
            'name': 'payement '+self.product_id.name,
            'facture_id': self.facture_id.id,
            'account_id': self.fournisseur_id.account_id.id or self.product_id.etablissement_fond.id,
            'exercice_id': self.facture_id.exercice_id.id,
            'debit': self.amount,
        })

        self.is_paid = True

class Pcmn(models.Model):
    _name = 'syndic.pcmn'
    _rec_name = 'code'
    name = fields.Char('Nom du compte', required=True)
    code = fields.Char('Code du compte', required=True)
    parent_id = fields.Many2one('syndic.pcmn', 'Compte parent')

    @api.multi
    def name_get(self):
        res = []
        for pcmn in self:
            name = "%s - %s" % (pcmn.name, pcmn.code)
            res += [(pcmn.id, name)]
        return res

class Prodcut(models.Model):
    _name = 'syndic.product'
    name = fields.Char('Produit')
    detail = fields.Text('Detail')
    payable_compte_id = fields.Many2one('syndic.pcmn', 'Compte payé')
    receive_compte_id = fields.Many2one('syndic.pcmn', 'Compte Reçu')
    etablissement_fond = fields.Many2one('syndic.pcmn', 'etabblissement de fond')
    accompte_fond_id = fields.Many2one('syndic.pcmn', 'etabblissement de fond')

class RepartitionLot(models.Model):
    _name = 'syndic.repartition.lot'
    name = fields.Char('Description', required=True)
    repart_detail_ids = fields.One2many('syndic.repartition.lot.detail', 'repartition_id', 'Detail de repartition')
    percentage_lot = fields.Float('Pourcentage des quotités', compute='compute_percentage_quot')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')

    @api.one
    def compute_percentage_quot(self):
        amount = 0.00
        for detail in self.repart_detail_ids:
            amount += detail.value
        self.percentage_lot = amount/10

    @api.one
    def create_normal_repartition(self):
        if not self.repart_detail_ids:
            for lot in self.immeuble_id.lot_ids:
                self.env['syndic.repartition.lot.detail'].create({
                    'lot_id': lot.id,
                    'value': lot.quotities,
                    'repartition_id': self.id,
                })
        else:
            raise exceptions.Warning('Il y a déjà des quotités.')


class BilanLigne(models.Model):
    _name = 'syndic.bilan.ligne'
    name = fields.Char('Description')
    debit = fields.Float('Debit')
    credit = fields.Float('Credit')
    total = fields.Float('Total')
    account_id = fields.Many2one('syndic.pcmn', 'Compte')
    facture_id = fields.Many2one('syndic.facture', 'Facture')
    exercice_id = fields.Many2one('syndic.exercice', 'Exercice')


class RepartitionLotDetail(models.Model):
    _name = 'syndic.repartition.lot.detail'
    _rec_name = 'lot_id'
    repartition_id = fields.Many2one('syndic.repartition.lot', 'Repartition Lot')
    value = fields.Float('Valeur')
    lot_id = fields.Many2one('syndic.lot', 'Lots')


class ExerciceCompta(models.Model):
    _name = 'syndic.exercice'
    name = fields.Char('Nom de l\'exercice')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')
    start_date = fields.Date('Date debut')
    end_date = fields.Date('Date fin')
    ligne_ids = fields.One2many('syndic.bilan.ligne', 'exercice_id', 'Ligne d\'exercice')
    state = fields.Selection([('draft', 'Brouillon'), ('open', 'Ouvert'), ('close', 'Cloturer')])

    @api.multi
    def open_exercice_wizard(self):
        return {
            'name': 'Ouverture d\'exercice',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'syndic.open.exercice.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': self._context,
        }

    @api.multi
    def close_exercice_wizard(self):
        return {
            'name': 'Cloture d\'exercice',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'syndic.close.exercice.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': self._context,
        }


class Fournisseur(models.Model):
    _inherit = 'syndic.supplier'
    account_id = fields.Many2one('syndic.pcmn', 'account')


class OpenExerciceWizard(models.TransientModel):
    _name = 'syndic.open.exercice.wizard'

    def _default_exercice(self):
        return self.env['syndic.exercice'].browse(self._context.get('active_id'))

    exercice_id = fields.Many2one('syndic.exercice', 'Exercice', default=_default_exercice)
    roulement_product_id = fields.Many2one('syndic.product', 'Produit fond de roulement')
    roulement = fields.Float('Fond de roulement')
    reserve_product_id = fields.Many2one('syndic.product', 'Produit fond de reserve')
    reserve = fields.Float('Fond de reserve')
    repartition_lot_id = fields.Many2one('syndic.repartition.lot', 'Répartition des Lots', required=True)

    @api.one
    def open_exercice(self):
        self.exercice_id.state = 'open'
        facture = self.env['syndic.facture'].create({
            'immeuble_id': self.exercice_id.immeuble_id.id,
            'exercice_id': self.exercice_id.id,
        })
        if self.roulement:
            self.env['syndic.facture.ligne'].create({
                'name': 'Etablissement de fonds de roulement',
                'amount': self.roulement,
                'invoice_line_date': datetime.date.today(),
                'repartition_lot_id': self.repartition_lot_id.id,
                'product_id': self.roulement_product_id.id,
                'facture_id': facture.id,
            })
        if self.reserve:
            self.env['syndic.facture.ligne'].create({
                'name': 'Etablissement de fonds de reserve',
                'amount': self.reserve,
                'invoice_line_date': datetime.date.today(),
                'repartition_lot_id': self.repartition_lot_id.id,
                'product_id': self.reserve_product_id.id,
                'facture_id': facture.id,
            })


class CloseExerciceWizard(models.TransientModel):
    _name = 'syndic.close.exercice.wizard'

    def _default_exercice(self):
        return self.env['syndic.exercice'].browse(self._context.get('active_id'))

    exercice_id = fields.Many2one('syndic.exercice', 'Exercice', default=_default_exercice)
    valeur_rapporter = fields.Float('Valeur à reporter')
    compte_rapporter = fields.Many2one('syndic.pcmn', 'Compte à reporter')
