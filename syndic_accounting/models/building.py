from odoo import api, fields, models


_MONTH = [
    ('1', 'Janvier'),
    ('2', 'Fevrier'),
    ('3', 'Mars'),
    ('4', 'Avril'),
    ('5', 'Mai'),
    ('6', 'Juin'),
    ('7', 'Juillet'),
    ('8', 'Aout'),
    ('9', 'Septembre'),
    ('10', 'Octobre'),
    ('11', 'Novembre'),
    ('12', 'Decembre')
]


class Building(models.Model):
    _inherit = 'syndic.building'

    period = fields.Selection([
        ('trimestrielle', 'Trimestriel'),
        ('annuel', 'Annuel'),
    ], 'Période')

    is_decompte_chauffage = fields.Boolean('Decompte Chauffage')
    is_decompte_eau = fields.Boolean('Decompte eau')
    date_cloture = fields.Selection(_MONTH, 'Mois de Cloture')

    accountant_id = fields.Many2one(
        'res.users',
        'Comptable',
        domain=[
            (
                'groups_id.name',
                'in',
                ['Syndic/Employe', 'Syndic/Manager']
            )
        ]
    )
