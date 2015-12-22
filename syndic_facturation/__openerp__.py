{
    'name': 'Facturation syndic',
    'version': '1.0',
    'category': 'Syndic',
    'description': """
    Facturation pour syndic
""",
    'author': 'OpenERP SA',
    'website': 'http://openerp.com',
    'depends': ['syndic_management', 'pdf_viewer'],
    'data': [
        'views/facturation.xml',
        'report/facture.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
    ],
    'auto_install': False,
    'installable': True,
}

