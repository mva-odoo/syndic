# -*- coding: utf-8 -*-
{
    'name': 'Appel',
    'version': '0.6',
    "category": 'Syndic',
    'description': """
    Gestion des appels
    """,
    'author': 'SGImmo',
    'depends': [
        'syndic_base',
    ],
    'data': [
        'views/claim_view.xml',
        'views/bon_commande.xml',
        'views/offre_contrat.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
}
