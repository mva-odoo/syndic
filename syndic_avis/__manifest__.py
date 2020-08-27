# -*- coding: utf-8 -*-

{
    'name': 'Syndic Avis',
    'version': '0.5',
    "category": 'Syndic',
    'description': """
    Syndic Avis
    """,
    'author': 'SGImmo SRL',
    'depends': ['syndic_base'],
    'website': 'https://www.sgimmo.be',
    'data': [
        'views/avis.xml',
        'report/avis.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
