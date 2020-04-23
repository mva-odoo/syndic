{
    'name': 'Facturation sgimmo',
    'version': '1.1',
    'category': 'Syndic',
    'description': """
    Facturation pour syndic
""",
    'author': 'odoo SA',
    'website': 'http://odoo.com',
    'depends': ['syndic_facturation'],
    'data': [
        'views/facturation_syndic.xml',
        'report/facture_sgimmo_report.xml',
        'security/ir.model.access.csv',
        'datas/facturation_type.xml',
    ],
    'installable': True,
}
