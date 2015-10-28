import openerplib

connexion_A = {
    'hostname': '127.0.0.1',
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
    'password': 'admin',
}

con_B = openerplib.get_connection(hostname=connexion_B['hostname'], database=connexion_B['database'],
                                         login=connexion_B['login'], password=connexion_B['password'])


def export_model(model_name, fields=[]):
    model = con_A.get_model(model_name)
    if not fields:
        fields = model.fields_get_keys()

    ids = model.search([('id', '!=', 1)])

    return model.export_data(ids, fields)


def import_model(model_name, fields, datas):
    model = con_B.get_model(model_name)

    if not fields:
        fields = model.fields_get_keys()

    return model.import_data(fields, datas)


normal_field = ['create_uid', 'create_date', 'write_uid', 'write_date']
# user
user_fields = ['id', 'name', 'login', 'password', 'signature', 'active']

export_datas = export_model("res.users", user_fields)
print export_datas
print '---------------------------------------------------------------------------------------------------------------'
print import_model("res.users", user_fields, export_datas['datas'])