{
    'name': 'Facturation syndic',
    'version': '1.0',
    'category': 'Syndic',
    'description': """
    Facturation pour syndic
""",
    'author': 'odoo SA',
    'website': 'http://odoo.com',
    'depends': ['syndic_base', 'pdf_viewer'],
    'data': [
        'views/facturation.xml',
        'report/facture.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'datas/sequence.xml',
        'wizards/generate_invoice.xml',
    ],
    'installable': True,
}

