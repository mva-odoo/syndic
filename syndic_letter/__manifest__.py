# -*- coding: utf-8 -*-

{
    'name': 'Syndic Letter',
    'version': '0.5',
    "category": 'Syndic',
    'description': """
    Syndic Lettre
    """,
    'author': 'odoo SA',
    'depends': ['syndic_base', 'mail', 'syndic_tools', 'pdf_viewer'],
    'website': 'https://www.sgimmo.be',
    'data': [
        'views/letter_view.xml',
        'report/letter.xml',
        'security/ir.model.access.csv',
    ],
}
