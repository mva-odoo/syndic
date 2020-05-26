# -*- coding: utf-8 -*-
{
    'name': 'Syndic Management',
    'version': '1.4.2.5',
    "category": 'Syndic',
    'description': """
    Syndic management:
    """,
    'author': 'SGIMMO',
    'depends': [
        'mail',
        'web_change',
        'base_address_city',
    ],
    'website': 'http://www.sgimmo.be',
    'data': [
            'views/fiche_signalitic.xml',
            'views/immeuble.xml',
            'views/metier.xml',
            'views/lot.xml',
            'views/mutation.xml',
            'views/setting.xml',
            'views/partner.xml',
            'views/proprietaire.xml',
            'views/locataire.xml',
            'views/fournisseur.xml',
            'views/res_users.xml',
            'views/menu.xml',
            'security/ir.model.access.csv',
            'security/groups.xml',
            'report/immeuble.xml',
        ],
    'application': True,
}
