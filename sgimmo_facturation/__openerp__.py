{
    'name': 'Facturation sgimmo',
    'version': '1.0',
    'category': 'Syndic',
    'description': """
    Facturation pour syndic
""",
    'author': 'OpenERP SA',
    'website': 'http://openerp.com',
    'depends': ['syndic_facturation'],
    'data': [
        'views/facturation_syndic.xml',
        'report/facture_sgimmo_report.xml',
        # 'security/groups.xml',
        # 'security/ir.model.access.csv',
    ],
    'installable': True,
}

