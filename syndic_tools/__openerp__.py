{
    'name': 'Syndic Tools',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Syndic Tools',
    'description': """
Syndic Tools
""",
    'author': 'Odoo SA',
    'depends': [
        'base',
    ],
    'data': [
        'views/deduplicate.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}

