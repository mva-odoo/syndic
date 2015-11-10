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
        'pages/gestion-de-copropriete.xml',
        'pages/gestion-privative.xml',
        'pages/contact.xml',
        'pages/consultance.xml',
        # 'pages/footer.xml',
        'views/res_users.xml'
        'views/website_change.xml'
    ],
    'auto_install': False,
    'installable': True,
}
