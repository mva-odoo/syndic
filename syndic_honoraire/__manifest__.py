# -*- coding: utf-8 -*-
{
    'name': 'Syndic Honoraire',
    'version': '1.0',
    'description': """
Honoraire for building
    """,
    'category': 'Syndic',
    'depends': [
        'syndic_invoice',
    ],
    'data': [
        'views/building.xml',
        'datas/index_year.xml',
        'wizard/honoraire.xml',
        'report/facture.xml',
        'security/ir.model.access.csv',
    ],

}
