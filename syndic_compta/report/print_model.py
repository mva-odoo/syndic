# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions

class Facture(models.TransientModel):
    _name = 'syndic.bilan.report.wizard'
    name = fields.Char('test')

    @api.multi
    def print_bilan(self):
        exercice = self.env['syndic.exercice'].browse(self._context['active_ids'])
        print exercice.ligne_ids.read_group(domain=[], fields={}, groupby='account_id')
        print exercice.read()[0]
        datas = {
            'ids': [self._context.get('active_id')],
            'model': 'syndic.exercice',
            'form': ['test', 'test'],
        }
        exercice.ligne_ids.read_group(domain=[], fields={}, groupby='account_id')
        return self.env['report'].get_action(exercice,
                                             'syndic_compta.syndic_compta_bilan',
                                             )
