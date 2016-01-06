# -*- coding: utf-8 -*-
{
    'name': 'Syndic calendar',
    'version': '0.1',
    "category": 'Syndic',
    'description': """
    calendar
    """,
    'author': 'OpenERP SA',
    'depends': ['web', 'syndic_management'],
    'website': 'http://www.openerp.com',
    'data': [
        'views/calendar.xml',
        'views/backend.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
}
