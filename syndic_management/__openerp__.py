# -*- coding: utf-8 -*-
{
    'name': 'Syndic Management',
    'version': '0.1',
    "category": 'Syndic',
    'description': """
    Syndic management:
    """,
    'author': 'SGIMMO',
    'depends': ['base', 'mail', 'syndic_tools'],
    'website': 'http://www.sgimmo.be',
    'data': [
            'views/fiche_signalitic.xml',
            'views/immeuble.xml',
            'views/metier.xml',
            'views/lot.xml',
            'views/supplier.xml',
            'views/owner.xml',
            'views/old_owner.xml',
            'views/loaner.xml',
            'views/other.xml',
            'views/mutation.xml',
            'views/setting.xml',
            'security/groups.xml',
            'views/menu.xml',
            'views/res_users.xml',
            # 'view/remove_menu.xml',
            'security/ir.model.access.csv',
        ],
    'application': True,
}
