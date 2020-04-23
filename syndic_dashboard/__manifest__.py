# -*- coding: utf-8 -*-
{
    'name': "Syndic dashboard",
    'summary': "Syndic dashboard",
    'description': """
        Syndic dashboard
    """,
    'version': '1.0',
    'depends': ['base', 'web', 'syndic_base'],
    'data': [
        'views/assets.xml',
        'views/dashboard.xml',
    ],
    'qweb': [
        'static/src/xml/dashboard.xml',
    ]
}
