{
    'name': 'Website sgimmo',
    'version': '1.0',
    'category': 'Syndic',
    'description': """
Site web SGImmo
""",
    'author': 'OpenERP SA',
    'website': 'http://openerp.com',
    'depends': ['website', 'syndic_documents'],
    'data': [
        'pages/document.xml',
        'pages/homepage.xml',
        'views/res_users.xml'
    ],
    'auto_install': False,
    'installable': True,
}
