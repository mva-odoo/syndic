# -*- coding: utf-8 -*-

{
    'name': 'Letter',
    'version': '0.1',
    "category": 'Event',
    'complexity': "easy",
    'description': """
    Syndic Lettre
    """,
    'author': 'OpenERP SA',
    'depends': ['syndic_management', 'mail', 'syndic_claim', 'syndic_tools'],
    'website': 'http://www.openerp.com',
    'data': [
        'view/letter_view.xml',
        'view/rapport_view.xml',
        'view/reunion.xml',
        'report/letter.xml',
        'report/avis.xml',
        'report/reunion.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}
