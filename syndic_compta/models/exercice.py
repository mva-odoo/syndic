# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
import datetime


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
    facture_id = fields.Many2one('syndic.facturation', 'Facture')
    exercice_id = fields.Many2one('syndic.exercice', 'Exercice')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')


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
    state = fields.Selection([('draft', 'Brouillon'),
                              ('open', 'Ouvert'),
                              ('amortissement', 'Amortissement'),
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
            'target': 'current',
            'context': self._context,
        }

    @api.multi
    def compte_resultat(self):
        for exercice in self:
            view_id = exercice.env.ref('syndic_compta.syndic_compte_resultat_compta_tree').id
            return {
                'name': 'Ouverture de vue regroupée ',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'syndic.bilan.ligne',
                'type': 'ir.actions.act_window',
                'view_id': view_id,
                'domain': ['|', ('account_id.code', '=ilike', '6%'), ('account_id.code', '=ilike', '7%')],
                'context': self.with_context(self.env.context, search_default_exercice_id=exercice.id,
                                             search_default_group_account=1).env.context,
            }

    @api.one
    def compute_amortissement(self):
        for facture in self.env['syndic.facturation'].search([('exercice_id', '=', self.id)]):
            for detail in facture.facture_detail_ids:
                if detail.is_amortissement:
                    for amortissement in detail.amortissement_ids:
                        if amortissement.counter != 0:
                            self.env['syndic.bilan.ligne'].create({
                                'name': 'amortissement',
                                'credit': amortissement.amount,
                                'account_id': amortissement.credit_account_id.id,
                                'exercice_id': self.id,
                                'immeuble_id': facture.immeuble_id.id,
                            })
                            self.env['syndic.bilan.ligne'].create({
                                'name': 'amortissement',
                                'debit': amortissement.amount,
                                'account_id': amortissement.debit_account_id.id,
                                'exercice_id': self.id,
                                'immeuble_id': facture.immeuble_id.id,
                            })
                            amortissement.counter = amortissement.counter-1
                            amortissement.stay_pay = amortissement.stay_pay - amortissement.amount

                            break
        self.state = 'amortissement'

    @api.multi
    def close_exercice_wizard(self):
        not_close_facture = self.env['syndic.facturation'].search([('exercice_id', '=', self.id),
                                                                   ('state', '!=', 'close')])
        if not_close_facture:
            names = [facture.name for facture in not_close_facture]
            raise exceptions.Warning('Toutes les factures ne sont pas cloturés %s' % names)

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
                'context': self.with_context(self.env.context,
                                             search_default_exercice_id=exercice.id,
                                             search_default_group_account=1).env.context,
            }


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
        return
        immeuble_id = self.env['syndic.exercice'].browse(self._context.get('active_id')).immeuble_id
        if self._context.get('reopen'):
            return immeuble_id.open_report_reserve_compte
        else:
            return immeuble_id.reserve_product_id

    def _default_product_roulement(self):
        return
        immeuble_id = self.env['syndic.exercice'].browse(self._context.get('active_id')).immeuble_id
        if self._context.get('reopen'):
            return immeuble_id.open_report_roulement_compte
        else:
            return immeuble_id.roulement_product_id

    exercice_id = fields.Many2one('syndic.exercice', 'Exercice', default=_default_exercice)
    roulement_product_id = fields.Many2one('syndic.facturation.type', 'Produit fond de roulement',
                                           default=_default_product_roulement)
    roulement = fields.Float('Fond de roulement')
    reserve_product_id = fields.Many2one('syndic.facturation.type', 'Produit fond de reserve',
                                         default=_default_product_reserve)
    reserve = fields.Float('Fond de reserve')
    repartition_lot_id = fields.Many2one('syndic.repartition.lot', 'Répartition des Lots')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble', default=_default_immeuble)

    @api.one
    def open_exercice(self):
        self.exercice_id.state = 'open'
        facture = self.env['syndic.facturation'].create({
            'immeuble_id': self.exercice_id.immeuble_id.id,
            'exercice_id': self.exercice_id.id,
        })
        if self.roulement:
            self.env['syndic.facturation.line'].create({
                'name': 'Etablissement de fonds de roulement',
                'prix': self.roulement,
                'invoice_line_date': datetime.date.today(),
                'repartition_lot_id': self.repartition_lot_id.id,
                'type_id': self.roulement_product_id.id,
                'facture_id': facture.id,
            })
        if self.reserve:
            self.env['syndic.facturation.line'].create({
                'name': 'Etablissement de fonds de reserve',
                'prix': self.reserve+self.exercice_id.amount_amortissement,
                'invoice_line_date': datetime.date.today(),
                'repartition_lot_id': self.repartition_lot_id.id,
                'type_id': self.reserve_product_id.id,
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
            exercice = self.env['syndic.exercice'].browse(wizard.env.context['active_id'])
            self.env['syndic.bilan.ligne'].create({
                'name': 'Cloture d exercice (fond de roulement)',
                'credit': wizard.roulement_valeur_rapporter,
                'account_id': wizard.roulement_compte_rapporter.id,
                'exercice_id': wizard.env.context['active_id'],
                'immeuble_id': exercice.immeuble_id.id,
            })
            self.env['syndic.bilan.ligne'].create({
                'name': 'Cloture d exercice (fond de reserve)',
                'credit': wizard.reserve_valeur_rapporter,
                'account_id': wizard.reserve_compte_rapporter.id,
                'exercice_id': wizard.env.context['active_id'],
                'immeuble_id': exercice.immeuble_id.id,
            })
            self.env['syndic.bilan.ligne'].create({
                'name': 'Cloture d exercice (valeur à reporter)',
                'debit': wizard.reserve_valeur_rapporter + wizard.roulement_valeur_rapporter,
                'account_id': wizard.compte_rapporter.id,
                'exercice_id': wizard.env.context['active_id'],
                'immeuble_id': exercice.immeuble_id.id,
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
            exercice = self.env['syndic.exercice'].browse(wizard._context['active_id'])
            self.env['syndic.bilan.ligne'].create({
                'name': 'Cloture d exercice (fond de roulement)',
                'credit': wizard.roulement_valeur_rapporter,
                'account_id': wizard.roulement_compte_rapporter.id,
                'exercice_id': wizard._context['active_id'],
                'immeuble_id': exercice.immeuble_id.id,
            })
            self.env['syndic.bilan.ligne'].create({
                'name': 'Cloture d exercice (fond de reserve)',
                'credit': wizard.reserve_valeur_rapporter,
                'account_id': wizard.reserve_compte_rapporter.id,
                'exercice_id': wizard.env.context['active_id'],
                'immeuble_id': exercice.immeuble_id.id,
            })
            self.env['syndic.bilan.ligne'].create({
                'name': 'Cloture d exercice (valeur à reporter)',
                'debit': wizard.reserve_valeur_rapporter + wizard.roulement_valeur_rapporter,
                'account_id': wizard.compte_rapporter.id,
                'exercice_id': wizard.env.context['active_id'],
                'immeuble_id': exercice.immeuble_id.id,
            })
            wizard.exercice_id.state = 'close'
