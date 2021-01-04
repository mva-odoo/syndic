from odoo import api, fields, models


class SyndicHonoraire(models.Model):
    _name = 'syndic.honoraire'
    _description = 'Honoraire'
    _rec_name = 'year_id'

    year_id = fields.Many2one('syndic.honoraire.year', string='Année', required=True)

    honoraire = fields.Float(string='Honoraire')
    frais_admin = fields.Float(string='Frais admin.')

    building_id = fields.Many2one('syndic.building', string='Immeuble')
    manager_id = fields.Many2one(related='building_id.manager_id', store=True)


class SyndicHonoraireYear(models.Model):
    _name = 'syndic.honoraire.year'
    _description = 'Honoraire Year'

    name = fields.Integer(string='Année', required=True)
    index = fields.Float('Index')

    honoraire_ids = fields.One2many('syndic.honoraire', 'year_id', string='Honoraires')

    def set_index(self):
        self.ensure_one()

        old_year = self.search([('name', '=', self.name-1)])
        coeff = self.index/old_year.index

        for honoraire in old_year.honoraire_ids:
            self.env['syndic.honoraire'].create({
                'year_id': self.id,
                'building_id': honoraire.building_id.id,
                'honoraire': honoraire.honoraire * coeff,
                'frais_admin': honoraire.frais_admin * coeff,
            })

    _sql_constraints = [(
            'name_unique',
            'UNIQUE(name)',
            "Année unique"
    )]