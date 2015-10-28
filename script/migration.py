import openerplib

connexion_A = {
    'hostname': 'openerp.sgimmo.be',
    'database': 'sgimmo',
    'login': 'admin',
    'password': 'Steroids1',
}


con_A = openerplib.get_connection(hostname=connexion_A['hostname'], database=connexion_A['database'],
                                         login=connexion_A['login'], password=connexion_A['password'])

connexion_B = {
    'hostname': '127.0.0.1',
    'database': 'sgimmo_migrate',
    'login': 'admin',
    'password': 'Steroids1',
}

con_B = openerplib.get_connection(hostname=connexion_B['hostname'], database=connexion_B['database'],
                                         login=connexion_B['login'], password=connexion_B['password'])


def export_model(model_name, fields=[], normal_field=True, domain=[]):
    model = con_A.get_model(model_name)
    if not fields:
        fields = model.fields_get_keys()
    else:
        if normal_field:
            fields += ['create_uid', 'create_date', 'write_uid', 'write_date']

    if domain:
        ids = model.search(domain)

    else:
        if model.name =='res.users':
            ids = model.search([('id', '!=', 1)])
        elif 'active' in fields:
            ids = model.search(['|', ('active', '=', True), ('active', '=', False)])
        else:
            ids = model.search([])

    fields.append('id')
    print fields
    return model.export_data(ids, fields)


def import_model(model_name, datas, fields=[], normal_field=True):
    model = con_B.get_model(model_name)

    if not fields:
        fields = model.fields_get_keys()
    else:
        if normal_field:
            fields += ['create_uid', 'create_date', 'write_uid', 'write_date']
    fields.append('id')
    print fields
    return model.import_data(fields, datas)


def export_import(model, fields=[], normal_field=True, domain=[]):
    export_datas = export_model(model, fields, normal_field, domain)
    print export_datas
    print '-------------------------------------------------------------------------------------------------------'
    print import_model(model, export_datas['datas'], fields, normal_field)



user_fields = ['name', 'login', 'password', 'signature', 'active']
export_import('res.users', user_fields, False, [('name', 'in', ['Administrator',
                                                                'Cindy',
                                                                'Serge',
                                                                'Florence',
                                                                'Sandrine'])])


export_import('city')
export_import('res.partner.title')
export_import('syndic.type_lot')
export_import('res.partner.job')
export_import('res.country', ['name'], False)

supplier = [
    'name',
    'title',
    'active',
    'street',
    'street2',
    'zip',
    'city/id',
    'state_id/id',
    'country_id/id',
    'email',
    'phone',
    'fax',
    'mobile',
    'city_id/id',
    'prenom',
    'gsm',
    #'job_ids',
]

export_import('syndic.supplier', supplier, False) #probleme de platrage
export_import('syndic.owner', supplier, False)
export_import('syndic.loaner', supplier, False)

export_datas = export_model('syndic.other', supplier, [])
print import_model('syndic.personne', export_datas['datas'], supplier, [])


building_fields = ['name',
                   'BCE',
                   'num_building',
                   'address_building',
                   'zip_building',
                   'city_building',
                   'compte',
                   'total_quotites',
                   'active',
                   'supplier_ids/id'
                   ]

export_import('syndic.building', building_fields, False)

lot_fields = [
    'name',
    'building_id/id',
    'proprio_id/id',
    'locataire_id/id',
    'quotities',
    'type_id/id',
]

export_import('syndic.lot', lot_fields, False)

export_import('syndic.old.owner', ['proprio_id/id', 'lot_ids/id', 'date_close'], False)