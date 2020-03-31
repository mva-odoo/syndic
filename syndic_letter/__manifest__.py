# -*- coding: utf-8 -*-

{
    'name': 'Syndic Letter',
    'version': '0.1',
    "category": 'Syndic',
    'description': """
    Syndic Lettre
    """,
    'author': 'odoo SA',
    'depends': ['syndic_management', 'mail', 'syndic_tools', 'pdf_viewer'],
    'website': 'http://www.odoo.com',
    'data': [
        'views/letter_view.xml',
        'views/reunion.xml',
        'views/avis.xml',
        'report/letter.xml',
        'report/avis.xml',
        'report/reunion.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
