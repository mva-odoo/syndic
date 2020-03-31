# -*- coding: utf-8 -*-
{
    'name': 'Syndic documents',
    'version': '0.1',
    "category": 'Syndic',
    'complexity': "easy",
    'description': """
    Syndic document
    """,
    'author': 'odoo SA',
    'depends': ['syndic_management'],
    'website': 'http://www.odoo.com',
    'data': [
        'views/syndic_document.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.csv',
        ],
    'installable': True,
}
