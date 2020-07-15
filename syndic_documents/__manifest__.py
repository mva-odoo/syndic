# -*- coding: utf-8 -*-
{
    'name': 'Syndic documents',
    'version': '0.5',
    "category": 'Syndic',
    'complexity': "easy",
    'description': """
    Syndic document
    """,
    'author': 'odoo SA',
    'depends': ['syndic_base'],
    'data': [
        'views/syndic_document.xml',
        'views/syndic_building.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.csv',
        ],
    'installable': True,
}
