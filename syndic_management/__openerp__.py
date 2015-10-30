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
            'view/fiche_signalitic.xml',
            'view/immeuble.xml',
            'view/metier.xml',
            'view/lot.xml',
            'view/supplier.xml',
            'view/owner.xml',
            'view/old_owner.xml',
            'view/loaner.xml',
            'view/other.xml',
            'view/mutation.xml',
            'view/setting.xml',
            'security/groups.xml',
            'view/menu.xml',
            'view/res_users.xml',
            # 'view/remove_menu.xml',
            'security/ir.model.access.csv',
        ],
    'application': True,
}
