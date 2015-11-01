# -*- coding: utf-8 -*-
{
    'name': 'Syndic calendar',
    'version': '0.1',
    "category": 'Syndic',
    'description': """
    calendar
    """,
    'author': 'OpenERP SA',
    'depends': ['syndic_management'],
    'website': 'http://www.openerp.com',
    'data': [
        'view/syndic_document.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.csv',
        ],
    'installable': True,
}
