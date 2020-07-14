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

    name = fields.Char(string='Année', required=True)
    index = fields.Float('Index')

    honoraire_ids = fields.One2many('syndic.honoraire', 'year_id', string='Honoraires')

    def set_index(self):
        for year in self:
            old_year = self.search([('id', '!=', year.id)], limit=1, order='id desc')
            for honoraire in old_year.honoraire_ids:
                print(honoraire.honoraire * (1 + (year.index)/100) if year.index else honoraire.honoraire)
                self.env['syndic.honoraire'].create({
                    'year_id': year.id,
                    'building_id': honoraire.building_id.id,
                    'honoraire': honoraire.honoraire * (1 + (year.index)/100) if year.index else honoraire.honoraire,
                    'frais_admin': honoraire.frais_admin * (1 + (year.index)/100) if year.index else honoraire.frais_admin,
                })
                
                