# -*- coding: utf-8 -*-

{
    'name': 'Syndic compta',
    'version': '0.1',
    "category": 'Syndic',
    'complexity': "easy",
    'description': """
    Gestion de la comptabilité des immeubles
    """,
    'author': 'OpenERP SA',
    'depends': ['syndic_management'],
    'website': 'http://www.openerp.com',
    'data': [
        'views/compta.xml',
        'views/fournisseurs.xml',
        'views/immeubles.xml',
        'report/print_report.xml',
        'report/bilan.xml',
    ],
    'installable': True,
    'active': False,
}
