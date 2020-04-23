# -*- coding: utf-8 -*-
from odoo import models, fields, exceptions


class SuiviFacture(models.TransientModel):
    _name = 'syndic.facturation.generation'
    _description = 'syndic.facturation.generation'

    def _get_immeuble(self):
        return self._context.get('active_ids', []) or []

    all_building = fields.Boolean('Tout les immeubles', default=True)
    index = fields.Float('Index')
    immeuble_ids = fields.Many2many('syndic.building', string='Immeubles', default=_get_immeuble)
    trimestre = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ], string='Trimestre', required=True)
    year = fields.Char(u'Année', required=True)
    date = fields.Date('Date', default=lambda *a: fields.date.today(), required=True)

    def invoice_generate(self):
        self.ensure_one()
        vals = {
           'date': self.date,
           'trimestre': self.trimestre,
           'year': self.year,
        }
        immeubles = self.immeuble_ids if self.immeuble_ids else self.env['syndic.building'].search([])

        for immeuble in immeubles:
            vals['immeuble_id'] = immeuble.id
            vals['facture_type'] = 'honoraire'
            vals['line_ids'] = [
               (0, 0, {
                   'name': 'Honoraires',
                   'prix': (immeuble.honoraire * self.index)/100 if self.index else immeuble.honoraire,
               })
            ]
            self.env['syndic.facturation'].create(vals)

            vals.pop('line_ids')
            vals.pop('facture_type')
            vals['facture_type'] = 'fraisadmin'

            vals['line_ids'] = [
               (0, 0, {
                   'name': 'Frais administratifs',
                   'prix': (immeuble.frais_admin * self.index) / 100 if self.index else immeuble.frais_admin,
               })
            ]
            self.env['syndic.facturation'].create(vals)
