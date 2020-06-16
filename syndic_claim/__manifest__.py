# -*- coding: utf-8 -*-
{
    'name': 'Appel',
    'version': '0.5',
    "category": 'Syndic',
    'complexity': "easy",
    'description': """
    Gestion des appels
    """,
    'author': 'SGImmo',
    'depends': ['syndic_base'],
    'website': 'http://www.odoo.com',
    'data': [
        'views/claim_view.xml',
        'report/barecode.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
}
