# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class WizardFacture(models.TransientModel):
    _name = 'syndic.bilan.report.wizard'
    name = fields.Char('test')


    @api.multi
    def _compute_lignes(self):
        exercice = self.env['syndic.exercice'].browse(self._context['active_ids'])
        create_ids = []
        for group_account in exercice.ligne_ids.read_group(domain=[], fields={}, groupby='account_id'):
            account = False

            if group_account.get('account_id'):
                account = group_account.get('account_id')[0]

            new_id = self.env['syndic.bilan.ligne.report.wizard'].create({
                'account_id': account,
                'credit': group_account['credit'],
                'debit': group_account['debit'],
                'total': group_account['total'],
            })

            create_ids.append(new_id.id)
        return [(6, 0, create_ids)]

    ligne_ids = fields.Many2many('syndic.bilan.ligne.report.wizard', string='Lignes',
                                 default=lambda self: self._compute_lignes())


    @api.multi
    def print_bilan(self):
        exercice = self.env['syndic.exercice'].browse(self._context['active_ids'])
        print exercice.ligne_ids.read_group(domain=[], fields={}, groupby='account_id')
        print exercice.read()[0]
        datas = {
            'ids': [self.id],
            'model': 'syndic.bilan.report.wizard',
            'form': ['test', 'test'],
        }
        exercice.ligne_ids.read_group(domain=[], fields={}, groupby='account_id')
        return self.env['report'].get_action(self,
                                             'syndic_compta.syndic_compta_bilan',
                                             )

    @api.multi
    def print_decompte_charge(self):
        exercice = self.env['syndic.exercice'].browse(self._context['active_ids'])

        datas = {
            'ids': [self._context.get('active_id')],
            'model': 'syndic.exercice',
            'form': ['test', 'test'],
        }
        exercice.ligne_ids.read_group(domain=[], fields={}, groupby='account_id')
        return self.env['report'].get_action(exercice,
                                             'syndic_compta.syndic_compta_decompte_charge',
                                             )


class WizardFactureGroup(models.TransientModel):
    _name = 'syndic.bilan.ligne.report.wizard'
    _rec_name = 'account_id'

    account_id = fields.Many2one('syndic.pcmn', 'Compte')
    credit = fields.Float('Credit')
    debit = fields.Float('Debit')
    total = fields.Float('Total')
