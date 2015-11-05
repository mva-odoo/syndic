{
    'name': 'PDF Viewer',
    'version': '1.0',
    'category': 'Syndic',
    'description': """
    see pdf
""",
    'author': 'OpenERP SA',
    'website': 'http://openerp.com',
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