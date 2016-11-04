# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Exrecice(models.Model):
    _name = 'syndic.compta.exercice'

    name = fields.Char('Exercice')
    open_date = fields.Date('Date d\'ouverture')
    close_date = fields.Date('Date de fermeture')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')
    is_current = fields.Boolean('Exercice courant')

    period_type = fields.Selection([
        ('trimestrielle', 'Trimestrielle'),
        ('annuelle', 'Annuelle'),
    ])
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('open', 'Ouvert'),
        ('amortissement', 'Amortissement'),
        ('close', 'Cloturer')], 'Etat', default='draft')

    exercice_ligne_ids = fields.One2many('syndic.compta.exercice.ligne', 'exercice_id', 'Lignes')
    # facture_ids = fields.One2many('syndic.compta.facture', 'exercice_id', 'Factures')
    # pcmn_id

    @api.multi
    def appel_fond(self):
        return {
            'name': 'Appel de fonds',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'syndic.compta.wizard.fond',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': self._context,
        }

    def close_exercice(self):
        pass

    def exercice_name(self):
        pass

    def compute_frais(self):
        pass

    def report_frais(self):
        pass


class ExerciceLigne(models.Model):
    _name = 'syndic.compta.exercice.ligne'
    _rec_name = 'account_id'

    account_id = fields.Many2one('syndic.compta.pcmn', 'Compte', required=True)
    debit = fields.Float('Débit')
    credit = fields.Float('Crédit')
    exercice_id = fields.Many2one('syndic.compta.exercice', 'Exercice')


class WizardFond(models.Model):
    _name = 'syndic.compta.wizard.fond'

    amount = fields.Float('Montant', required=True)
    type = fields.Selection([('reserve', 'Réserve'), ('roulement', 'Roulement')], 'Type de fond', required=True)
    is_facturable = fields.Boolean('Création de facture', default=True)
    account_id = fields.Many2one('syndic.compta.pcmn', 'Compte', required=True)
    accompte_account_id = fields.Many2one('syndic.compta.pcmn', 'Compte d\'accompte', required=True,
                                          help='le compte d\'accompte: 4101 --> roulement, 4100 --> résèrve')
    is_split_accompte = fields.Boolean('Spliter compte d\'accompte',
                                       help="permet de voir qui as payé directement dans la compta")

    @api.multi
    def create_fond(self):
        self.ensure_one()
        self.env['syndic.compta.exercice.ligne'].create({
            'debit': self.amount,
            'credit': 0,
            'account_id': self.accompte_account_id.id,
            'exercice_id': self._context.get('active_id'),
        })

        self.env['syndic.compta.exercice.ligne'].create({
            'debit': 0,
            'credit': self.amount,
            'account_id': self.account_id.id,
            'exercice_id': self._context.get('active_id'),
        })

        if self.is_facturable:
            facture = self.env['syndic.compta.facture'].create({
                'name': str('Création de fonds de %s') % str(self.type),
            })
            self.env['syndic.compta.facture.ligne'].create({
                'facture_id': facture.id,
                'amount': self.amount,
                'qty': 1,
            })