# -*- coding: utf-8 -*-

{
    'name': 'Appel',
    'version': '0.1',
    "category": 'Syndic',
    'complexity': "easy",
    'description': """
    Gestion des appels
    """,
    'author': 'OpenERP SA',
    'depends': ['syndic_management'],
    'website': 'http://www.openerp.com',
    'data': [
	'view/claim_view.xml',
    'security/ir.model.access.csv',
        ],
    'installable': True,
    'active': False,
    'application' : False,
    'certificate': '',
    'images': [],
}
