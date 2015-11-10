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


print '-------------------------------------------------------------------------------------------------------'
print 'syndic.mutation'
export_datas = export_model('syndic.mutation', [
    'mutation_date',
    'old_owner_id/id',
    'new_owner_id/id',
    'lot_ids/id',
    'state',
    'immeuble_id/id',
  ], [])

print import_model('syndic.mutation', export_datas['datas'], [
    'mutation_date',
    'old_owner_ids/id',
    'new_owner_ids/id',
    'lot_ids/id',
    'state',
    'immeuble_id/id',
  ], [])

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


letter = ['begin_letter_id/id', 'create_date', 'save_letter', 'is_fax',
          'name_template', 'create_uid/id', 'end_letter_id/id', 'state', 'sujet',
          'immeuble_id/id', 'letter_type_id/id', 'name', 'contenu',  'ps',
          'date', 'date_fr', 'write_date', 'write_uid/id', 'all_immeuble', 'mail_server/id', 'is_mail',
          'partner_address_ids/id', 'letter_model_id/id', 'loc_ids/id',
          'fourn_ids/id',
          'old_ids/id', 'divers_ids/id',
          'propr_ids/id',
          ]

print '-------------------------------------------------------------------------------------------------------'
print 'letter.letter'
export_datas = export_model('letter.create', letter, [])
print import_model('letter.letter', export_datas['datas'], letter, [])

export_import('reunion.type')
export_import('letter.reunion', ['name', 'immeuble_id/id', 'descriptif',
                                 'create_date', 'write_date', 'type_id/id', 'date', 'date_fr'], False)
export_import('reunion.point', ['name', 'sequence',
                                'reunion_id/id', 'descriptif'], False)
export_import('type.avis')
export_import('letter.avis', ['name',
                              'text',
                              'immeuble_id/id',
                              'create_date',
                              'write_date',
                              'date',
                              'date_fr',
                              'type_id/id',
                              'avis_model_id/id',
                              ], False)

 # ficher signalitique

sign = ['ascensseur_contrat', 'jardin_more', 'marque_citerne', 'write_uid', 'garden_more',
        'notaire_building', 'toiture_type', 'toiture_contract', 'risque_expirt',
        'egoutage_more', 'justice', 'technique', 'number_parking', 'chauffage_cascade',
        'type_citerne', 'chassis_more', 'building_id/id', 'extincteur_more', 'garden_travaux',
        'chassis_color', 'garden_day', 'date_compteur', 'nettoyage_more', 'condensation_chauffage',
        'parlophone_description', 'descriptif_tache', 'compte', 'elec_contrat',
        'compta', 'date_mois', 'amiente_etabli_par', 'garage_contrat_date',
        'parlophone_bool', 'ascensseur_le', 'chaudiere_omnium', 'number_cave', 'contrat_chaudiere',
        'type_adoucisseur', 'number_appartement', 'create_date', 'date_quizaine', 'citerne_par',
        'appartements_bool', 'juridique', 'chauffage_type', 'conciergerie', 'egoutage_contrat',
        'plaquette_supplier', 'type_chauffage', 'incendie_expire', 'jardin_contrat', 'garden_contract',
        'elec_expirt', 'sol_expire', 'facade_isolation', 'access_info', 'type_chauffages', 'risque_le',
        'adoucisseur_more', 'descr_regul', 'ascenseur', 'chaudiere_entretien_date', 'date_cloture',
        'boite_bool', 'sol_date', 'supplier_adoucisseur', 'annee_adoucisseur', 'chauffage',
        'plan_egout', 'qte_citerne', 'chaudiere_more', 'incendie_name_courier',
        'ascenseur_bool', 'risque_ascensseur_par', 'elec_releve_by', 'access_where', 'lieu_assemble',
        'chassis_vitrage_four', 'last_peint_date', 'elec_building', 'construction_date', 'qte_adoucisseur',
        'firm_name_netoyage', 'eau_chaude_type', 'create_uid', 'sol_inscription', 'societe_compteur',
        'firm_netoyage_date', 'loi', 'date_contrat_compteur', 'peb_immeuble', 'chaudiere_tubage',
        'entretien_nettoyage', 'entr_control', 'more_info', 'citerne_neutralise', 'cylindre_bool',
        'parlophone_date', 'rec_creance', 'incendie_num_police', 'incendie_couverture', 'elec_le',
        'ascensseur_par', 'lieu_acte_building', 'certif_chauf', 'travaux_realise',
        'mur_mitoyens', 'ramassage', 'garden_firm',
        'number_chambres', 'chassis_type', 'annee_citerne', 'trotoire', 'prepose_netoyage', 'date_jardin',
        'ascensseur_date', 'id', 'plan_appartement', 'incendie_franchise', 'chassis_vitrage',
        'anne_ascensseur', 'environnement_objet', 'access_more', 'garage_contrat',
        'chaudiere_separboue', 'parlophone_more', 'nbr_passage', 'amiente_etabli_le',
        'anne_chaudiere', 'environnement_expire', 'chaudiere_horloge', 'garage_description', 'ass_concierge',
        'numeros_adoucisseur', 'date_acte_building', 'incendie_name', 'ramassage_type',
        'garden_tree', 'marque_adoucisseur', 'write_date', 'nbr_chaudiere', 'elec_par',
        'environnement_date', 'citerne_le', 'plan_sous_sol', 'egoutage_contrat_date',
        'situation_chauffage', 'plan_facade', 'citerne_expirt', 'ascensseur_more', 'ramassage_date',
        'toiture_isolation', 'number_garage']

export_import('building.signalitic', sign, False)



export_import('building.desamientage', [
    'desamiente_par/id',
    'desamiente_le',
    'desamiente_niveau',
    'signalitic_id/id',
], False)

export_import('building.diu')
export_import('building.facade')
export_import('facade.repair')
export_import('building.terasse')
export_import('building.repeir.terasse')
export_import('observation.toiture')
export_import('repeir.toiture')
export_import('jardin.observation')
export_import('ascensseurs')
export_import('repeir.ascensseur')
export_import('piece.chauffage')
export_import('egoutage.observation')
export_import('extincteur')
export_import('repeir.garage')
export_import('repeir.general')


# calendrier

print '-------------------------------------------------------------------------------------------------------'
print 'syndic.calendar'
export_datas = export_model('calendar.event', [
    'name',
    'start_date',
    'stop_date',
    'user_id/id',
    'location',
    'description',
  ], [])

print import_model('syndic.calendar', export_datas['datas'], [
    'name',
    'start_date',
    'end_date',
    'owner_id/id',
    'where',
    'description',
  ], [])