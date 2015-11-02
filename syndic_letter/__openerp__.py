# -*- coding: utf-8 -*-

{
    'name': 'Syndic Letter',
    'version': '0.1',
    "category": 'Syndic',
    'description': """
    Syndic Lettre
    """,
    'author': 'OpenERP SA',
    'depends': ['syndic_management', 'mail', 'syndic_tools'],
    'website': 'http://www.openerp.com',
    'data': [
        'views/letter_view.xml',
        'views/reunion.xml',
        'report/letter.xml',
        'report/avis.xml',
        'report/reunion.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}