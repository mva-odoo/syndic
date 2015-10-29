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
    'database': 'sgimmo9',
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
    return model.export_data(ids, fields)


def import_model(model_name, datas, fields=[], normal_field=True):
    model = con_B.get_model(model_name)

    if not fields:
        fields = model.fields_get_keys()
    else:
        if normal_field:
            fields += ['create_uid', 'create_date', 'write_uid', 'write_date']
    fields.append('id')
    return model.import_data(fields, datas)


def export_import(model, fields=[], normal_field=True, domain=[]):
    export_datas = export_model(model, fields, normal_field, domain)
    print '-------------------------------------------------------------------------------------------------------'
    # print export_datas
    print model
    print import_model(model, export_datas['datas'], fields, normal_field)

export_import('res.groups', ['name'], False)
user_fields = ['name',
               'login',
               'password',
               'signature',
               'active',
               'groups_id/id']

export_import('res.users', user_fields, False, [('name', 'in', ['Administrator',
                                                                'Cindy',
                                                                'Serge',
                                                                'Florence',
                                                                'Sandrine'
                                                                ])])




export_import('city')
export_import('res.partner.title', ['name'], False)
export_import('syndic.type_lot')
export_import('res.partner.job')
export_import('res.country', ['name'], False)

personne = [
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
]

supplier = personne + ['job_ids/id']
export_import('syndic.supplier', supplier, False)
owner = personne + ['convocation', 'password']
export_import('syndic.owner', owner, False)
export_import('syndic.loaner', personne, False)

print '-------------------------------------------------------------------------------------------------------'
print 'syndic.personne'
export_datas = export_model('syndic.other', personne, [])
print import_model('syndic.personne', export_datas['datas'], personne, [])


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
export_import('partner.address', ['name',
                                  'city_id/id',
                                  'title/id',
                                  'street',
                                  'street2',
                                  'zip',
                                  'city',
                                  'state_id/id',
                                  'country_id/id',
                                  'email',
                                  'phone',
                                  'fax',
                                  'mobile',
                                  'active',
                                  'add_parent_id_owner/id',
                                  'add_parent_id_supplier/id',
                                  'supplier_id/id',
                                  'add_parent_id_loaner/id',
                                  'is_letter',
                                  ], False)

export_import('syndic.mutation', ['mutation_date',
                                  'old_owner_id/id',
                                  'new_owner_id/id',
                                  'lot_ids/id',
                                  'state',
                                  'immeuble_id/id',
                                  ], False)


# --------------------------------
# claim
# --------------------------------
export_import('claim.type')
export_import('claim.status')


claim = [
    'subject',
    'email',
    'phone',
    'create_date',
    'write_date',
    'create_uid/id',
    'write_uid/id',
    'manager_id/id',
    'main_owner/id',
    'owner_ids/id',
    'supplier_ids/id',
    'loaner_ids/id',
    'other_ids/id',
    'lot_ids/id',
    'claim_status_id/id',
    'building_id/id',
    'importance',
    'color',
    'status',
    'type_id/id',
    ]

export_import('syndic.claim', claim, False)

export_import('comment.history', ['name', 'description',
                                  'current_status/id', 'claim_ids/id'], False)
export_import('bon.commande', ['name',
                               'immeuble_id/id',
                               'fournisseur_id/id',
                               'date_demande',
                               'cloture',
                               'date_cloture',
                               ], False)

export_import('offre.contrat')

# --------------------------------
# facturation
# --------------------------------

export_import('syndic.qty.type')
export_import('syndic.facturation.type')
export_import('syndic.facturation', ['date_fr',
                                     'name',
                                     'immeuble_id/id',
                                     'object',
                                     'date',
                                     'total',
                                     ], False)
export_import('syndic.facturation.line', ['prix_tot',
                                          'facture_id/id',
                                          'type_id/id',
                                          'qty_id',
                                          'prix',
                                          'nombre',
                                          'name'], False)

# --------------------------------
# letter
# --------------------------------
export_import('letter.avis.model')
export_import('letter.model')
export_import('letter.type')
export_import('letter.begin')
export_import('letter.end')
