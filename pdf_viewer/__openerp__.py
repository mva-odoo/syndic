{
    'name': 'PDF Viewer',
    'version': '1.0',
    'category': 'Syndic',
    'description': """
    see pdf
""",
    'author': 'Odoo SA',
    'website': 'http://odoo.com',
    'depends': ['web'],
    'data': [
        'backend.xml',
        'action.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'auto_install': True,
    'installable': True,
}