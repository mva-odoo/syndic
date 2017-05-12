# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Desamientage(models.Model):
    _name = 'building.desamientage'
    desamiente_par = fields.Many2one('syndic.supplier', string='Désamianté par')
    desamiente_le = fields.Date('Désamianté le')
    desamiente_niveau = fields.Char('au niveau de')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitique')


class DIU(models.Model):
    _name = 'building.diu'
    diu_par = fields.Many2one('syndic.supplier', string='DIU par')
    diu_le = fields.Date('DIU le')
    diu_concerne = fields.Char('Concerne')
    diu_id = fields.Many2one('building.signalitic', string='DIU')


class ObservationFacade(models.Model):
    _name = 'building.facade'
    observation = fields.Text('Observation')
    date_observation = fields.Date("Date d'observation")
    suivi = fields.Text("Suivi")
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class RepeirFacade(models.Model):
    _name = 'facade.repair'
    facade_date_repeir = fields.Date('date de la réparation')
    facade_fournisseur_repeir = fields.Many2one('syndic.supplier', string='entreprise')
    facade_what_repeir = fields.Text('Objet de la réparation')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class Terasse(models.Model):
    _name = 'building.terasse'
    observation = fields.Text('Observation')
    date_observation = fields.Date("Date d'observation")
    suivi = fields.Text("suivi")
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class RepeirTerasse(models.Model):
    _name = 'building.repeir.terasse'
    terasse_date_repeir = fields.Date('date de la réparation')
    terasse_fournisseur_repeir = fields.Many2one('syndic.supplier', string='entreprise')
    terasse_what_repeir = fields.Text('Objet de la réparation')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class ObservationToiture(models.Model):
    _name = 'observation.toiture'
    observation_toiture = fields.Char('Observation')
    date_toiture = fields.Date("Date de l'observation")
    suivi_toiture = fields.Char('Suivi')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class RepeirToiture(models.Model):
    _name = 'repeir.toiture'
    entreprise = fields.Many2one('syndic.supplier', string='Fournisseur')
    date_repeir = fields.Date('Date')
    objet_repeir = fields.Char('Objet de la réparation')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class ObservationJardin(models.Model):
    _name = 'jardin.observation'
    observation_jardin = fields.Char('Observation')
    date_jardin = fields.Date("Date de l'observation")
    suivi_jardin = fields.Char('Suivi')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class Ascensseur(models.Model):
    _name = 'ascensseurs'
    name = fields.Char('Ascenseur')
    type = fields.Char('Type')
    vitesse = fields.Char('Vitesse')
    constructeur = fields.Char('Constructeur')
    date_asc = fields.Integer('Année de fabrication')
    charge = fields.Integer('Charge maximale')
    nbr_personne = fields.Integer('Nombre de personnes maximales')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class RepeirAscensseur(models.Model):
    _name = 'repeir.ascensseur'
    entreprise = fields.Many2one('syndic.supplier', string='Fournisseur')
    date_repeir = fields.Date('Date')
    objet_repeir = fields.Char('Objet de la réparation')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class PieceChauffage(models.Model):
    _name = "piece.chauffage"
    parties = fields.Selection([
                               ('crops', 'Corps de chauffe'),
                               ('bruleur', 'Bruleur'),
                               ('circulateur', 'Circulateur'),
                               ('vase', 'Vase d\'expension'),
                               ('regul', 'Régulateur')], 'Parties')
    Marque = fields.Char('Marque')
    type = fields.Char('Type')
    annee = fields.Integer('Année de construction')
    puissance = fields.Char('Puissance')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class RepeirChaudiere(models.Model):
    _name = 'repeir.chaudiere'
    entreprise = fields.Many2one('syndic.supplier', string='Fournisseur')
    date_repeir = fields.Date('Date')
    objet_repeir = fields.Char('Objet de la réparation')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class ObservationEgoutage(models.Model):
    _name = 'egoutage.observation'
    entreprise = fields.Many2one('syndic.supplier', string='Fournisseur')
    date_egoutage = fields.Date("Date de l'observation")
    suivi_egoutage = fields.Char('objet de la réparation')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class Extincteur(models.Model):
    _name = 'extincteur'
    extincteur_marque = fields.Char('Marque')
    extincteur_contrat = fields.Many2one('syndic.supplier', string='Contrat d\'entretien')
    extincteur_contrat_date = fields.Date('date anniversaire du contrat')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class RepeirGarage(models.Model):
    _name = 'repeir.garage'
    entreprise = fields.Many2one('syndic.supplier', string='Fournisseur')
    date_repeir = fields.Date('Date')
    objet_repeir = fields.Char('Objet de la réparation')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class RepeirGeneral(models.Model):
    _name = 'repeir.general'
    entreprise = fields.Many2one('syndic.supplier', string='Fournisseur')
    date_repeir = fields.Date('Date')
    objet_repeir = fields.Char('Objet de la réparation')
    architect = fields.Many2one('syndic.supplier', string='architect')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class SignalitiqueImmeuble(models.Model):
    _name = 'building.signalitic'
    _inherits = {'syndic.building': 'building_id'}

    building_id = fields.Many2one('syndic.building', string='Immeuble', required=True)
    # info general---------------------------------------
    construction_date = fields.Integer('Date de construction')
    date_mois = fields.Selection([('janvier', 'Janvier'), ('fevrier', 'Fevrier'), ('mars', 'Mars'), ('avril', 'Avril'),
                                  ('mai', 'Mai'), ('juin', 'Juin'), ('juillet', 'Juillet'), ('aout', 'Aout'),
                                  ('septembre', 'Septembre'), ('octobre', 'Octobre'), ('novembre', 'Novembre'),
                                  ('decembre', 'Decembre')], 'Mois')
    date_quizaine = fields.Selection([('1', '1'), ('2', '2')], 'Quinzaine')
    lieu_assemble = fields.Char('Lieu de la tenue de l assemblee generale')
    compte = fields.Char('Compte bancaire')
    compta = fields.Selection([('trimestrielle', 'Trimestrielle'), ('annuelle', 'Annuelle')], 'Comptabilite')
    date_cloture = fields.Selection(
        [('janvier', 'Janvier'), ('fevrier', 'Fevrier'), ('mars', 'Mars'), ('avril', 'Avril'), ('mai', 'Mai'),
         ('juin', 'Juin'), ('juillet', 'Juillet'), ('aout', 'Aout'), ('septembre', 'Septembre'),
         ('octobre', 'Octobre'), ('novembre', 'Novembre'), ('decembre', 'Decembre')],
        'Date de cloture de la comptabilite')
    # acte de base
    notaire_building = fields.Char('Notaire')
    lieu_acte_building = fields.Char('Lieu de transcription')
    date_acte_building = fields.Date('Date de transcription')
    # plan
    plan_sous_sol = fields.Boolean('Plan sous sol')
    plan_facade = fields.Boolean('Plan facade')
    plan_appartement = fields.Boolean('Plan appartement')
    plan_egout = fields.Boolean('Plan réseaux d\'egoutage')

    # nombres lots
    number_appartement = fields.Integer("Nombre d appartements")
    number_garage = fields.Integer("Nombre de boxes garages")
    number_cave = fields.Integer("Nombre de caves")
    number_chambres = fields.Integer("Nombre de chambres de bonnes")
    number_parking = fields.Integer("Nombre d'emplacements")
    conciergerie = fields.Boolean('Conciergerie')
    # assurances
    # incendie
    incendie_name = fields.Char('Nom de la compagnie')
    incendie_name_courier = fields.Char('Nom du courtier')
    incendie_num_police = fields.Char('N° de la police')
    incendie_franchise = fields.Selection([('legal', 'Legal'), ('extra_legal', 'Extra Legal')], 'Franchise')
    incendie_expire = fields.Date('Expire le')
    incendie_couverture = fields.Text('Couverture')

    loi = fields.Boolean('Assurance loi')
    justice = fields.Boolean('Assurance défense en justice')
    ass_concierge = fields.Boolean('Assurance concièrge')
    rec_creance = fields.Boolean('Assurance recouvrement de créance')

    # 2-------------------------------------------------------------------------------------
    # expert technique
    technique = fields.Many2one('syndic.supplier', 'Expert technique')
    chauffage = fields.Many2one('syndic.supplier', 'Expert chauffage ')
    ascenseur = fields.Many2one('syndic.supplier', 'Expert ascenseur')
    certif_chauf = fields.Many2one('syndic.supplier', 'Certificateur chauffage')
    juridique = fields.Many2one('syndic.supplier', 'Avocat')
    environnement_date = fields.Date('Délivré le')
    environnement_expire = fields.Date('Expire le')
    environnement_objet = fields.Text('Objets')

    # sol
    sol_inscription = fields.Boolean('Classé en zone pollué')
    sol_date = fields.Date('Etude de sol établi le')
    sol_expire = fields.Date('Expire le')
    # inventaire amiante
    amiente_etabli_par = fields.Many2one('syndic.supplier', 'Etabli par')
    amiente_etabli_le = fields.Date('Etabli le')
    amiente_ids = fields.One2many('building.desamientage', 'signalitic_id', 'Désamientage')
    # citerne
    citerne_par = fields.Many2one('syndic.supplier', 'Etabli par')
    citerne_le = fields.Date('Établi le')
    citerne_expirt = fields.Date('Expire le')
    citerne_neutralise = fields.Boolean('Citerne neutralisé')
    # electricité
    elec_par = fields.Many2one('syndic.supplier', 'Etabli par')
    elec_le = fields.Date('Établi le')
    elec_expirt = fields.Date('Expire le')
    # risque
    risque_ascensseur_par = fields.Many2one('syndic.supplier', 'Etabli par')
    risque_le = fields.Date('Établi le')
    risque_expirt = fields.Date('Expire le')
    # ascensseur
    anne_ascensseur = fields.Integer("Année de construction de l'assensseur")
    ascensseur_par = fields.Many2one('syndic.supplier', 'Executé par')
    ascensseur_le = fields.Date('Attestation de conformité établi le')
    # chauffage
    diu = fields.One2many('building.diu', 'diu_id', 'DIU')
    anne_chaudiere = fields.Integer('Année de construction de la chaudière')
    peb_immeuble = fields.Boolean("Existance d'un audit de chauffage de plus de 15ans")
    # info service
    ramassage = fields.Selection(
        [('individuel', 'Individuel'), ('copropriete', 'copropriete'), ('bxl_prop', 'Bruxelles propreté'),
         ('private', 'privé')], 'Ramassage')
    ramassage_type = fields.Selection([('sac', 'Par sac'), ('contenaire', 'Par contenairs')], 'Type de ramassage')
    ramassage_date = fields.Selection(
        [('lundi', 'Lundi'), ('mardi', 'Mardi'), ('mercredi', 'Mercredi'), ('jeudi', 'Jeudi'),
         ('vendredi', 'Vendredi'), ('samedi', 'Samedi'), ('dimanche', 'Dimanche')], 'Jour de ramassage')
    # jardins
    garden_contract = fields.Boolean('Contrats d entretien des espaces vert')
    garden_firm = fields.Char('Nom')
    garden_day = fields.Date('Date')
    garden_tree = fields.Text('Arbre à abattre')
    garden_travaux = fields.Text('Travaux')
    garden_more = fields.Text('description travaux')
    # nettoyage
    entretien_nettoyage = fields.Selection([('individuel', 'indivuduel'), ('collectif', 'Collectif')])
    firm_name_netoyage = fields.Char('Nom de la firme')
    firm_netoyage_date = fields.Datetime('Jour de passage')
    prepose_netoyage = fields.Char('Jour de passage')
    descriptif_tache = fields.Char('Descriptif des taches')
    last_peint_date = fields.Date('Dernière mise en peinture')
    travaux_realise = fields.Text('Travaux réalisés ')
    nettoyage_more = fields.Text('Informations supplémentaires')
    # 3-------------------------------------------------------------------------------------
    # info immeuble
    # abord
    trotoire = fields.Text('Trottoirs')
    mur_mitoyens = fields.Text('Mur mitoyens')
    more_info = fields.Text('Informations supplémentaires et observations particulières')

    # facade
    facade_id = fields.One2many('building.facade', 'signalitic_id', string='Facade')
    facade_isolation = fields.Boolean('Isolation')
    facade_repeir_id = fields.One2many('facade.repair', 'signalitic_id', string='Reparation facade')
    # chassis
    chassis_type = fields.Selection([('bois', 'bois'), ('pvc', 'pvc'), ('alu', 'alu')], string='Type de chassis')
    chassis_vitrage = fields.Selection([('simple', 'simple'), ('double', 'double')], string='Vitrage')
    chassis_vitrage_four = fields.Char('Fabricant')
    chassis_color = fields.Char('Couleur')
    chassis_more = fields.Text('Informations supplémentaires et observations particulières')
    # terasse
    terasse_ids = fields.One2many('building.terasse', 'signalitic_id', string='Terasse')
    terasse_repeir_ids = fields.One2many('building.repeir.terasse', 'signalitic_id', string='Terasse')
    # access
    access_info = fields.Text('Porte d’entrée: informations et descriptions')
    access_where = fields.Many2one('syndic.supplier', 'Certificat pour la reproduction de clé')
    access_more = fields.Text('Informations et descriptions')

    # parlophone et boite
    plaquette_supplier = fields.Many2one('syndic.supplier', 'Société de plaquettes')
    parlophone_description = fields.Text('Parlophonie: informations et descriptions')
    parlophone_date = fields.Date('Dernière mise à jour des plaquettes')
    parlophone_more = fields.Text('Informations supplémentaires et observations particulières ')
    boite_bool = fields.Boolean('Plaquettes boites')
    ascenseur_bool = fields.Boolean('Plaquettes ascensseur')
    appartements_bool = fields.Boolean('Plaquettes appartements')
    parlophone_bool = fields.Boolean('Plaquettes parlophone')

    # toiture
    toiture_type = fields.Char('Type')
    toiture_contract = fields.Char("Contrat d'entretien")
    toiture_obs = fields.One2many('observation.toiture', 'signalitic_id', string='Observation')
    toiture_isolation = fields.Boolean('Isolation')
    toiture_repa = fields.One2many('repeir.toiture', 'signalitic_id', string='Observation')

    # jardin
    jardin_contrat = fields.Many2one('syndic.supplier', 'Contrat d\'entretien')
    date_jardin = fields.Date('Date anniversaire du contrat jardin')
    jardin_onservation = fields.One2many('jardin.observation', 'signalitic_id', string='Observation jardin')
    jardin_more = fields.Text('Informations supplémentaires')

    # ascensseur
    ascensseur_contrat = fields.Many2one('syndic.supplier', 'Contrat d\'entretien')
    ascensseur_date = fields.Date('Date anniversaire du contrat')
    nbr_passage = fields.Integer('Nombre de passage par an')
    ascensseur_ids = fields.One2many('ascensseurs', 'signalitic_id', string='Ascenseurs')
    repeir_ascensseur_ids = fields.One2many('repeir.ascensseur', 'signalitic_id', string='Réparation ascensseur')
    cylindre_bool = fields.Boolean('cylindre')
    entr_control = fields.Many2one('syndic.supplier', 'Société de contrôle')
    ascensseur_more = fields.Text('Observation complémentaires')

    # compteur
    societe_compteur = fields.Many2one('syndic.supplier', 'Société')
    date_compteur = fields.Selection(
        [('janvier', 'Janvier'), ('fevrier', 'Fevrier'), ('mars', 'Mars'), ('avril', 'Avril'), ('mai', 'Mai'),
         ('juin', 'Juin'), ('juillet', 'Juillet'), ('aout', 'Aout'), ('septembre', 'Septembre'),
         ('octobre', 'Octobre'), ('novembre', 'Novembre'), ('decembre', 'Decembre')], 'mois')
    date_contrat_compteur = fields.Date('Date anniversaire du contrat')

    # chauffage
    chauffage_type = fields.Selection([('individuel', 'Individuel'),
                                       ('collectif', 'Collectif')], 'Type de chauffage')
    eau_chaude_type = fields.Selection([('individuel', 'Individuel'),
                                        ('collectif', 'Collectif')], 'Production eau chaude')
    type_chauffage = fields.Selection([('gaz', 'Gaz'),
                                       ('mazoutb', 'Mazout type b'),
                                       ('mazoutc', 'Mazout type c')], 'Type')
    condensation_chauffage = fields.Boolean('A condensation ')
    type_chauffages = fields.Char('Autre type')
    situation_chauffage = fields.Text('Situation')
    nbr_chaudiere = fields.Integer('Nombre de chaudiere')
    chauffage_cascade = fields.Boolean('Chaudière en cascade')
    contrat_chaudiere = fields.Many2one('syndic.supplier', 'Contrat d\'entretien')
    chaudiere_entretien_date = fields.Date('Date anniversaire d\'entretien chaudiere')
    chaudiere_omnium = fields.Boolean('Contrat omnium')
    chaudiere_tubage = fields.Boolean('Tubage de la cheminée')
    chaudiere_separboue = fields.Boolean('Séparateur de boues')
    chaudiere_horloge = fields.Boolean('Horloge')
    piece_chaudiere_ids = fields.One2many('piece.chauffage', 'signalitic_id', string='Pièce chauffage')
    descr_regul = fields.Text('Description de la régulation')
    repeir_chaudiere_ids = fields.One2many('repeir.chaudiere', 'signalitic_id', string='Réparation chaudière')
    chaudiere_more = fields.Text('Observation complémentaire')

    # adoussisseur
    type_adoucisseur = fields.Char('Type d adoucisseur')
    marque_adoucisseur = fields.Char('Marque adoucisseur')
    numeros_adoucisseur = fields.Char('Numeros adoucisseur')
    annee_adoucisseur = fields.Integer('Année de construction')
    supplier_adoucisseur = fields.Many2one('syndic.supplier', 'Contrat d\'entretien')
    qte_adoucisseur = fields.Integer('Quantité généralement commandées')
    adoucisseur_more = fields.Text('Observations')

    # Citerne
    marque_citerne = fields.Char('Marque')
    type_citerne = fields.Char('Type')
    annee_citerne = fields.Date('Date du contrôle')
    qte_citerne = fields.Integer('Capacité de la citerne')

    # egoutage
    egoutage_contrat = fields.Many2one('syndic.supplier', 'Contrat d\'entretien')
    egoutage_contrat_date = fields.Date('Date anniversaire du contrat')
    obs_egoutage_ids = fields.One2many('egoutage.observation', 'signalitic_id', string="Réparations egoutages")
    egoutage_more = fields.Text("Informations supplémentaires et observations particulières")

    # extincteur
    extincteur_ids = fields.One2many('extincteur', 'signalitic_id', 'Extincteurs')
    extincteur_more = fields.Text('observations particulières')

    # instal elec
    elec_contrat = fields.Many2one('syndic.supplier', 'Contrat d\'entretien')
    elec_building = fields.Many2one('syndic.supplier', 'electricien du bâtiment')
    elec_releve_by = fields.Char('Relevé par')

    # garage
    garage_contrat = fields.Many2one('syndic.supplier', 'Contrat d\'entretien')
    garage_contrat_date = fields.Date('date anniversaire du contrat')
    garage_repeir_ids = fields.One2many('repeir.garage', 'signalitic_id', string='Réparation garage')
    garage_description = fields.Text('Observations complémentaires')

    # travaux
    travaux_ids = fields.One2many('repeir.general', 'signalitic_id', string='Travaux')

    @api.onchange('building_id')
    def _onchange_check_exist(self):
        if self.search([('building_id', '=', self.building_id.id)]):
            return {'warning': {'message': 'Attention: Ce bâtiment à deja une fiche signalitique'}}
        return {}

    _sql_constraints = [
        ('model_id_field_id_uniq', 'unique (building_id)', ("Ce bâtiment à deja une fiche signalitique!"))
    ]
