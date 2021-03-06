# -*- coding: utf-8 -*-
{
    'name': 'Syndic Management',
    'version': '1.4.2.5',
    "category": 'Syndic/Syndic',
    'description': """
    Syndic management:
    """,
    'author': 'SGIMMO',
    'depends': [
        'mail',
        'web_change',
        'base_address_city',
        'contacts',
        'syndic_tools',
    ],
    'website': 'http://www.sgimmo.be',
    'data': [
            'security/groups.xml',
            'security/ir.model.access.csv',
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
            'views/contract.xml',
            'views/menu.xml',
            'views/quotity.xml',
            'report/immeuble.xml',
            'datas/res.city.csv',
            'datas/title.xml',
        ],
    'demo': [
        'demos/users.xml',
        'demos/building.xml',
    ],
    'application': True,
}
