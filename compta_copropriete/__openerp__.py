# -*- coding: utf-8 -*-

{
    'name': 'Comptabilite de copropriéte',
    'version': '0.1',
    "category": 'Syndic',
    'description': """
    Gestion de la comptabilite des immeubles
    """,
    'author': 'OpenERP SA',
    'depends': ['syndic_management'],
    'website': 'http://www.openerp.com',
    'data': [
        'views/exercice.xml',
        'views/appel_fond.xml',
        'views/facture.xml',
        'views/building.xml',
        'views/payment.xml',
        'views/fournisseurs.xml',
    ],
    'installable': True,
    'active': False,
}