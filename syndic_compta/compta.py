# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
import datetime

class Facture(models.Model):
    _name = 'syndic.facture'

    @api.depends('immeuble_id')
    @api.one
    def _compute_exercice(self):
        self.exercice_id = self.immeuble_id.current_exercice_id

    name = fields.Char('Facture numeros')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble', required=True)
    invoice_date = fields.Date('Date de facture')
    facture_line_ids = fields.One2many('syndic.facture.ligne', 'facture_id', 'Ligne de facture')
    state = fields.Selection([('draft', 'Brouillon'), ('validate', 'Validé'), ('close', 'Fermé')],
                             'Etat', default='draft')
    facture_detail_ids = fields.One2many('syndic.facture.detail', 'facture_id', 'Detail de facture')
    bilan_ids = fields.One2many('syndic.bilan.ligne', 'facture_id', 'Lignes du bilan')
    exercice_id = fields.Many2one('syndic.exercice', 'Exercice', compute=_compute_exercice, required=True)
    proprietaire_ids = fields.Many2many('syndic.owner', string='Proprietaires')

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
                            # proprio_ids = [proprio_id.id for proprio_id in repartition_line.lot_id.proprio_id]
                            proprio_ids = repartition_line.lot_id.proprio_id
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


class FactureLigne(models.Model):
    _name = 'syndic.facture.ligne'

    name = fields.Char('Description', required=True)
    amount = fields.Float('Montant', required=True)
    invoice_line_date = fields.Date('Date d\'echéhance')
    fournisseur_id = fields.Many2one('syndic.supplier', 'Fournisseur')
    product_id = fields.Many2one('syndic.product', 'Produit', required=True)
    repartition_lot_id = fields.Many2one('syndic.repartition.lot', 'Répartition des Lots')
    facture_id = fields.Many2one('syndic.facture', 'Facture')


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
            self.split_amount = self.env['syndic.facture.detail'].browse(self._context.get('active_id')).amount / self.duration
        else:
            self.split_amount = 0.00

    product_id = fields.Many2one('syndic.product', 'Produit', default=_default_product)
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

    product_id = fields.Many2one('syndic.product', 'Produit')
    active = fields.Boolean('Actif', default=True)
    amount = fields.Float('Montant')
    number = fields.Integer('Numeros de l\'accompte')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')
    facture_detail_id = fields.Many2one('syndic.facture.detail', 'Detail de facture')
    debit_account_id = fields.Many2one('syndic.pcmn', 'Compte de Debis pour l\'amortissement')
    credit_account_id = fields.Many2one('syndic.pcmn', 'Compte de Credit pour l\'amortissement')
    stay_pay = fields.Float('Reste à payer')
    counter = fields.Integer('Compteur')


class Pcmn(models.Model):
    _name = 'syndic.pcmn'
    _rec_name = 'code'
    name = fields.Char('Nom du compte', required=True)
    code = fields.Char('Code du compte', required=True)
    parent_id = fields.Many2one('syndic.pcmn', 'Compte parent')
    main_compte = fields.Boolean('Compte Général')
    type_account = fields.Selection([('roulement', 'Roulement'), ('reserve', 'Reserve')])

    @api.multi
    def name_get(self):
        res = []
        for pcmn in self:
            name = "%s-%s" % (pcmn.code, pcmn.name)
            res += [(pcmn.id, name)]
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            args = ['|', ('name', operator, name), ('code', operator, name)] + args
        pcmn = self.search(args, limit=limit)
        return pcmn.name_get()

class Prodcut(models.Model):
    _name = 'syndic.product'
    name = fields.Char('Produit')
    detail = fields.Text('Detail')
    payable_compte_id = fields.Many2one('syndic.pcmn', 'Compte payé')
    receive_compte_id = fields.Many2one('syndic.pcmn', 'Compte Reçu')
    etablissement_fond = fields.Many2one('syndic.pcmn', 'etabblissement de fond')
    accompte_fond_id = fields.Many2one('syndic.pcmn', 'accompte de fond')
    account_product = fields.Boolean('Produit comptable')

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

    @api.depends('debit', 'credit')
    @api.multi
    def _compute_total(self):
        for bilan_ligne in self:
            bilan_ligne.total = bilan_ligne.debit - bilan_ligne.credit

    name = fields.Char('Description')
    debit = fields.Float('Debit')
    credit = fields.Float('Credit')
    total = fields.Float('Total', compute=_compute_total, store=True)
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

    @api.one
    def _compute_amortissement(self):
        detail_ids = self.env['syndic.facture.detail'].search([('facture_id.exercice_id', '=', self.id)]).ids
        amount = 0.00
        for amortissement in self.env['syndic.compta.amortissement'].search([('facture_detail_id', 'in', detail_ids)]):
            amount += amortissement.stay_pay
        self.amount_amortissement = amount

    name = fields.Char('Nom de l\'exercice')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')
    start_date = fields.Date('Date debut')
    end_date = fields.Date('Date fin')
    ligne_ids = fields.One2many('syndic.bilan.ligne', 'exercice_id', 'Ligne d\'exercice')
    amount_amortissement = fields.Float('Amortissement', compute=_compute_amortissement)
    state = fields.Selection([('draft', 'Brouillon'), ('open', 'Ouvert'), ('amortissement', 'Amortissement'),
        ('close', 'Cloturer')], 'Etat', default='draft')

    @api.one
    def reset(self):
        self.state = 'draft'

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
    def print_bilan(self):
        return {
            'name': 'Imprimer le bilan',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'syndic.bilan.report.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': self._context,
        }

    @api.multi
    def compte_resultat(self):
        for exercice in self:
            view_id = exercice.env.ref('syndic_compta.syndic_compte_resultat_compta_tree').id
            print view_id
            return {
                'name': 'Ouverture de vue regroupée ',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'syndic.bilan.ligne',
                'type': 'ir.actions.act_window',
                'view_id': view_id,
                'domain': ['|', ('account_id.code', '=ilike', '6%'), ('account_id.code', '=ilike', '7%')],
                'context': self.with_context(self._context, search_default_exercice_id=exercice.id,
                                             search_default_group_account=1)._context,
            }

    @api.one
    def compute_amortissement(self):
        for facture in self.env['syndic.facture'].search([('exercice_id', '=', self.id)]):
            for detail in facture.facture_detail_ids:
                if detail.is_amortissement:
                    for amortissement in detail.amortissement_ids:
                        if amortissement.counter != 0:
                            self.env['syndic.bilan.ligne'].create({
                                'name': 'amortissement',
                                'credit': amortissement.amount,
                                'account_id': amortissement.credit_account_id.id,
                                'exercice_id': self.id,
                            })
                            self.env['syndic.bilan.ligne'].create({
                                'name': 'amortissement',
                                'debit': amortissement.amount,
                                'account_id': amortissement.debit_account_id.id,
                                'exercice_id': self.id,
                            })
                            amortissement.counter = amortissement.counter-1
                            amortissement.stay_pay = amortissement.stay_pay - amortissement.amount

                            break
        self.state = 'amortissement'


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

    @api.multi
    def open_group_exercice(self):
        for exercice in self:
            return {
                'name': 'Ouverture de vue regroupée ',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'syndic.bilan.ligne',
                'type': 'ir.actions.act_window',
                'context': self.with_context(self._context, search_default_exercice_id=exercice.id,
                                             search_default_group_account=1)._context,
            }

class Fournisseur(models.Model):
    _inherit = 'syndic.supplier'
    account_id = fields.Many2one('syndic.pcmn', 'account')


class OpenExerciceWizard(models.TransientModel):
    _name = 'syndic.open.exercice.wizard'

    def _default_exercice(self):
        if self._context.get('reopen'):
            return False
        else:
            return self.env['syndic.exercice'].browse(self._context.get('active_id'))

    def _default_immeuble(self):
        return self.env['syndic.exercice'].browse(self._context.get('active_id')).immeuble_id

    def _default_product_reserve(self):
        immeuble_id = self.env['syndic.exercice'].browse(self._context.get('active_id')).immeuble_id
        if self._context.get('reopen'):
            return immeuble_id.open_report_reserve_compte
        else:
            return immeuble_id.reserve_product_id

    def _default_product_roulement(self):
        immeuble_id = self.env['syndic.exercice'].browse(self._context.get('active_id')).immeuble_id
        if self._context.get('reopen'):
            return immeuble_id.open_report_roulement_compte
        else:
            return immeuble_id.roulement_product_id

    exercice_id = fields.Many2one('syndic.exercice', 'Exercice', default=_default_exercice)
    roulement_product_id = fields.Many2one('syndic.product', 'Produit fond de roulement',
                                           default=_default_product_roulement)
    roulement = fields.Float('Fond de roulement')
    reserve_product_id = fields.Many2one('syndic.product', 'Produit fond de reserve',
                                         default=_default_product_reserve)
    reserve = fields.Float('Fond de reserve')
    repartition_lot_id = fields.Many2one('syndic.repartition.lot', 'Répartition des Lots')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble', default=_default_immeuble)

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
                'amount': self.reserve+self.exercice_id.amount_amortissement,
                'invoice_line_date': datetime.date.today(),
                'repartition_lot_id': self.repartition_lot_id.id,
                'product_id': self.reserve_product_id.id,
                'facture_id': facture.id,
            })


        self.exercice_id.immeuble_id.current_exercice_id = self.exercice_id

class CloseExerciceWizard(models.TransientModel):
    _name = 'syndic.close.exercice.wizard'

    def _default_exercice(self):
        return self.env['syndic.exercice'].browse(self._context.get('active_id'))

    def _default_immeuble(self):
        return self.env['syndic.exercice'].browse(self._context.get('active_id')).immeuble_id

    def _default_report_roulement(self):
        immeuble_id = self.env['syndic.exercice'].browse(self._context.get('active_id')).immeuble_id
        return immeuble_id.report_roulement_compte

    def _default_report_reserve(self):
        immeuble_id = self.env['syndic.exercice'].browse(self._context.get('active_id')).immeuble_id
        return immeuble_id.report_reserve_compte

    def _default_report(self):
        immeuble_id = self.env['syndic.exercice'].browse(self._context.get('active_id')).immeuble_id
        return immeuble_id.compte_rapporter

    def _default_report_roulement_value(self):
        exercice_id = self.env['syndic.exercice'].browse(self._context.get('active_id')).id
        immeuble_id = self.env['syndic.exercice'].browse(self._context.get('active_id')).immeuble_id
        account_fond = immeuble_id.roulement_product_id.etablissement_fond.id
        amount = 0.00
        for compte in self.env['syndic.bilan.ligne'].search([('exercice_id', '=', exercice_id),
                                                             ('account_id', '=', account_fond)]):
            amount += compte.debit-compte.credit
        return amount

    def _default_report_reserve_value(self):
        exercice_id = self.env['syndic.exercice'].browse(self._context.get('active_id'))
        immeuble_id = self.env['syndic.exercice'].browse(self._context.get('active_id')).immeuble_id
        account_fond = immeuble_id.reserve_product_id.etablissement_fond.id
        amount = 0.00
        for compte in self.env['syndic.bilan.ligne'].search([('exercice_id', '=', exercice_id.id),
                                                             ('account_id', '=', account_fond)]):
            amount += compte.debit-compte.credit
        return amount+exercice_id.amount_amortissement

    exercice_id = fields.Many2one('syndic.exercice', 'Exercice', default=_default_exercice)
    roulement_valeur_rapporter = fields.Float('Valeur de fond de roulement à reporter',
                                              default=_default_report_roulement_value)
    reserve_valeur_rapporter = fields.Float('Valeur de fond de reserve à reporter',
                                            default=_default_report_reserve_value)
    compte_rapporter = fields.Many2one('syndic.pcmn', 'Compte à reporter',
                                       default=_default_report)
    reserve_compte_rapporter = fields.Many2one('syndic.pcmn', 'Compte de fond de reserve à reporter',
                                               default=_default_report_reserve)
    roulement_compte_rapporter = fields.Many2one('syndic.pcmn', 'Compte de fond de roulement à reporter',
                                                 default=_default_report_roulement)
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble', default=_default_immeuble)

    @api.multi
    def close_exercice_reopen(self):
        for wizard in self:
            self.env['syndic.bilan.ligne'].create({
                'name': 'Cloture d exercice (fond de roulement)',
                'credit': wizard.roulement_valeur_rapporter,
                'account_id': wizard.roulement_compte_rapporter.id,
                'exercice_id': wizard._context['active_id'],
            })
            self.env['syndic.bilan.ligne'].create({
                'name': 'Cloture d exercice (fond de reserve)',
                'credit': wizard.reserve_valeur_rapporter,
                'account_id': wizard.reserve_compte_rapporter.id,
                'exercice_id': wizard._context['active_id'],
            })
            self.env['syndic.bilan.ligne'].create({
                'name': 'Cloture d exercice (valeur à reporter)',
                'debit': wizard.reserve_valeur_rapporter + wizard.roulement_valeur_rapporter,
                'account_id': wizard.compte_rapporter.id,
                'exercice_id': wizard._context['active_id'],
            })
            wizard.exercice_id.state = 'close'

            context = self.with_context(self._context, default_reserve=wizard.reserve_valeur_rapporter,
                                        default_roulement=wizard.roulement_valeur_rapporter,
                                        reopen=1)._context



        return {
            'name': 'Ouverture d\'exercice',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'syndic.open.exercice.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
        }

    @api.multi
    def close_exercice(self):
        for wizard in self:
            self.env['syndic.bilan.ligne'].create({
                'name': 'Cloture d exercice (fond de roulement)',
                'credit': wizard.roulement_valeur_rapporter,
                'account_id': wizard.roulement_compte_rapporter.id,
                'exercice_id': wizard._context['active_id'],
            })
            self.env['syndic.bilan.ligne'].create({
                'name': 'Cloture d exercice (fond de reserve)',
                'credit': wizard.reserve_valeur_rapporter,
                'account_id': wizard.reserve_compte_rapporter.id,
                'exercice_id': wizard._context['active_id'],
            })
            self.env['syndic.bilan.ligne'].create({
                'name': 'Cloture d exercice (valeur à reporter)',
                'debit': wizard.reserve_valeur_rapporter + wizard.roulement_valeur_rapporter,
                'account_id': wizard.compte_rapporter.id,
                'exercice_id': wizard._context['active_id'],
            })
            wizard.exercice_id.state = 'close'



class SyndicComptaSetting(models.Model):
    _inherit = 'syndic.building'

    roulement_product_id = fields.Many2one('syndic.product', 'Produit d ouverture (roulement)')
    reserve_product_id = fields.Many2one('syndic.product', 'Produit d ouverture (resrve)')
    compte_rapporter = fields.Many2one('syndic.pcmn', 'Compte à reporter')
    report_reserve_compte = fields.Many2one('syndic.pcmn', 'Compte de fond de reserve à reporter')
    report_roulement_compte = fields.Many2one('syndic.pcmn', 'Compte de fond de roulement à reporter')
    open_report_reserve_compte = fields.Many2one('syndic.product', 'Produit de fond de reserve à reporter pour reouverture')
    open_report_roulement_compte = fields.Many2one('syndic.product', 'Produit de fond de roulement à reporter pour reouverture')
    # immeuble_id = fields.Many2one('syndic.building', 'Immeuble')
    current_exercice_id = fields.Many2one('syndic.exercice', 'Exercice courant')