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
    'depends': ['syndic_facturation'],
    'website': 'http://www.openerp.com',
    'data': [
        'views/compta.xml',
        'views/fournisseurs.xml',
        'views/immeubles.xml',
        'views/lot.xml',
        'views/facture.xml',
        'views/amortissement.xml',
        'views/exercice.xml',
        'views/pcmn.xml',
        'views/produit.xml',
        'views/repartition.xml',
        'report/print_report.xml',
        'report/bilan.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'active': False,
}
