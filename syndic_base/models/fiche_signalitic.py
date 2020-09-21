# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class Desamientage(models.Model):
    _name = 'building.desamientage'
    _description = 'building.desamientage'
    desamiente_par = fields.Many2one('res.partner', string=u'Désamianté par')
    desamiente_le = fields.Date(u'Désamianté le')
    desamiente_niveau = fields.Char('au niveau de')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitique')


class ObservationFacade(models.Model):
    _name = 'building.facade'
    _description = 'building.facade'
    observation = fields.Text('Observation')
    date_observation = fields.Date("Date d'observation")
    suivi = fields.Text("Suivi")
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class RepeirFacade(models.Model):
    _name = 'facade.repair'
    _description = 'facade.repair'
    facade_date_repeir = fields.Date(u'date de la réparation')
    facade_fournisseur_repeir = fields.Many2one('res.partner', string='entreprise')
    facade_what_repeir = fields.Text(u'Objet de la réparation')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class Terasse(models.Model):
    _name = 'building.terasse'
    _description = 'building.terasse'
    observation = fields.Text('Observation')
    date_observation = fields.Date("Date d'observation")
    suivi = fields.Text("suivi")
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class RepeirTerasse(models.Model):
    _name = 'building.repeir.terasse'
    _description = 'building.repeir.terasse'
    terasse_date_repeir = fields.Date(u'date de la réparation')
    terasse_fournisseur_repeir = fields.Many2one('res.partner', string='entreprise')
    terasse_what_repeir = fields.Text(u'Objet de la réparation')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class ObservationToiture(models.Model):
    _name = 'observation.toiture'
    _description = 'observation.toiture'
    observation_toiture = fields.Char('Observation')
    date_toiture = fields.Date("Date de l'observation")
    suivi_toiture = fields.Char('Suivi')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class RepeirToiture(models.Model):
    _name = 'repeir.toiture'
    _description = 'repeir.toiture'
    entreprise = fields.Many2one('res.partner', string='Fournisseur')
    date_repeir = fields.Date('Date')
    objet_repeir = fields.Char(u'Objet de la réparation')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class ObservationJardin(models.Model):
    _name = 'jardin.observation'
    _description = 'jardin.observation'
    observation_jardin = fields.Char('Observation')
    date_jardin = fields.Date("Date de l'observation")
    suivi_jardin = fields.Char('Suivi')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class Ascensseur(models.Model):
    _name = 'ascensseurs'
    _description = 'ascensseurs'
    name = fields.Char('Ascenseur')
    type = fields.Char('Type')
    vitesse = fields.Char('Vitesse')
    constructeur = fields.Char('Constructeur')
    date_asc = fields.Integer(u'Année de fabrication')
    charge = fields.Integer('Charge maximale')
    nbr_personne = fields.Integer('Nombre de personnes maximales')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class RepeirAscensseur(models.Model):
    _name = 'repeir.ascensseur'
    _description = 'repeir.ascensseur'
    entreprise = fields.Many2one('res.partner', string='Fournisseur')
    date_repeir = fields.Date('Date')
    objet_repeir = fields.Char(u'Objet de la réparation')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class PieceChauffage(models.Model):
    _name = "piece.chauffage"
    _description = "piece.chauffage"
    parties = fields.Selection([
                               ('crops', 'Corps de chauffe'),
                               ('bruleur', 'Bruleur'),
                               ('circulateur', 'Circulateur'),
                               ('vase', 'Vase d\'expension'),
                               ('regul', 'Régulateur')], 'Parties')
    Marque = fields.Char('Marque')
    type = fields.Char('Type')
    annee = fields.Integer(u'Année de construction')
    puissance = fields.Char('Puissance')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class RepeirChaudiere(models.Model):
    _name = 'repeir.chaudiere'
    _description = 'repeir.chaudiere'
    entreprise = fields.Many2one('res.partner', string='Fournisseur')
    date_repeir = fields.Date('Date')
    objet_repeir = fields.Char(u'Objet de la réparation')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class ObservationEgoutage(models.Model):
    _name = 'egoutage.observation'
    _description = 'egoutage.observation'
    entreprise = fields.Many2one('res.partner', string='Fournisseur')
    date_egoutage = fields.Date("Date de l'observation")
    suivi_egoutage = fields.Char(u'objet de la réparation')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class Extincteur(models.Model):
    _name = 'extincteur'
    _description = 'extincteur'
    extincteur_marque = fields.Char('Marque')
    extincteur_contrat = fields.Many2one('res.partner', string='Contrat d\'entretien extincteur')
    extincteur_contrat_date = fields.Date('date anniversaire du contrat extincteur')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class RepeirGarage(models.Model):
    _name = 'repeir.garage'
    _description = 'repeir.garage'
    entreprise = fields.Many2one('res.partner', string='Fournisseur')
    date_repeir = fields.Date('Date')
    objet_repeir = fields.Char(u'Objet de la réparation')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class RepeirGeneral(models.Model):
    _name = 'repeir.general'
    _description = 'repeir.general'
    entreprise = fields.Many2one('res.partner', string='Fournisseur')
    date_repeir = fields.Date('Date')
    objet_repeir = fields.Char(u'Objet de la réparation')
    architect = fields.Many2one('res.partner', string='architect')
    signalitic_id = fields.Many2one('building.signalitic', string='signalitic')


class SignalitiqueImmeuble(models.Model):
    _name = 'building.signalitic'
    _description = 'building.signalitic'
    _inherits = {'syndic.building': 'building_id'}

    building_id = fields.Many2one('syndic.building', string='Fiche Immeuble', required=True, ondelete="cascade")
    # info general---------------------------------------
    construction_date = fields.Integer('Date de construction')

    lieu_assemble = fields.Char('Lieu de la tenue de l assemblee generale')
    compte = fields.Char('Compte bancaire')
    compta = fields.Selection([('trimestrielle', 'Trimestrielle'), ('annuelle', 'Annuelle')], 'Comptabilite')
    date_cloture = fields.Selection(
        [('janvier', 'Janvier'), ('fevrier', 'Fevrier'), ('mars', 'Mars'), ('avril', 'Avril'), ('mai', 'Mai'),
         ('juin', 'Juin'), ('juillet', 'Juillet'), ('aout', 'Aout'), ('septembre', 'Septembre'),
         ('octobre', 'Octobre'), ('novembre', 'Novembre'), ('decembre', 'Decembre')],
        u'Date de cloture de la comptabilite')
    # acte de base
    notaire_building = fields.Char('Notaire')
    lieu_acte_building = fields.Char('Lieu de transcription')
    date_acte_building = fields.Date('Date de transcription')
    # plan
    plan_sous_sol = fields.Boolean('Plan sous sol')
    plan_facade = fields.Boolean('Plan facade')
    plan_appartement = fields.Boolean('Plan appartement')
    plan_egout = fields.Boolean(u'Plan réseaux d\'egoutage')

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
    incendie_num_police = fields.Char(u'N° de la police')
    incendie_franchise = fields.Selection([('legal', 'Legal'), ('extra_legal', 'Extra Legal')], 'Franchise')
    incendie_expire = fields.Date('Expiration Incendie')
    incendie_couverture = fields.Text('Couverture')

    loi = fields.Boolean('Assurance loi')
    justice = fields.Boolean(u'Assurance défense en justice')
    ass_concierge = fields.Boolean(u'Assurance concièrge')
    rec_creance = fields.Boolean(u'Assurance recouvrement de créance')

    # 2-------------------------------------------------------------------------------------
    # expert technique
    technique = fields.Many2one('res.partner', 'Expert technique')
    chauffage = fields.Many2one('res.partner', u'Expert chauffage')
    ascenseur = fields.Many2one('res.partner', 'Expert ascenseur')
    certif_chauf = fields.Many2one('res.partner', 'Certificateur chauffage')
    juridique = fields.Many2one('res.partner', 'Avocat')
    environnement_date = fields.Date(u'Délivré le')
    environnement_expire = fields.Date('Expiration Environnement')
    environnement_objet = fields.Text('Objets')

    # sol
    sol_inscription = fields.Boolean(u'Classé en zone pollué')
    sol_date = fields.Date(u'Etude de sol établi le')
    sol_expire = fields.Date('Sol Expire le')
    # inventaire amiante
    amiente_etabli_par = fields.Many2one('res.partner', 'Amiente Etabli par')
    amiente_etabli_le = fields.Date('Amiente Etabli le')
    amiente_ids = fields.One2many('building.desamientage', 'signalitic_id', u'Désamientage')
    # citerne
    citerne_par = fields.Many2one('res.partner', 'Citerne Etabli par')
    citerne_le = fields.Date(u'Établi le')
    citerne_expirt = fields.Date('Citerne Expire le')
    citerne_neutralise = fields.Boolean(u'Citerne neutralisé')
    # electricité
    elec_par = fields.Many2one('res.partner', 'Electricite Etabli par')
    elec_le = fields.Date(u'Electrecite Établi le')
    elec_expirt = fields.Date('Electrecite Expire le')
    # risque
    risque_ascensseur_par = fields.Many2one('res.partner', 'Risque Ascensseur Etabli par')
    risque_le = fields.Date(u'Risque Établi le')
    risque_expirt = fields.Date('Risque Expire le')
    # ascensseur
    anne_ascensseur = fields.Integer(u"Année de construction de l'assensseur")
    ascensseur_par = fields.Many2one('res.partner', u'Executé par')
    ascensseur_le = fields.Date(u'Attestation de conformité établi le')
    # chauffage
    anne_chaudiere = fields.Integer(u'Année de construction de la chaudière')
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
    garden_day = fields.Date("Date d'entretien")
    garden_tree = fields.Text(u'Arbre à abattre')
    garden_travaux = fields.Text('Travaux jardin')
    garden_more = fields.Text('description travaux')
    # nettoyage
    entretien_nettoyage = fields.Selection([('individuel', 'indivuduel'), ('collectif', 'Collectif')])
    firm_name_netoyage = fields.Char('Nom de la firme')
    firm_netoyage_date = fields.Datetime('Date Jour de passage')
    prepose_netoyage = fields.Char('Preposé Jour de passage')
    descriptif_tache = fields.Char('Descriptif des taches')
    last_peint_date = fields.Date(u'Dernière mise en peinture')
    travaux_realise = fields.Text(u'Travaux réalisés ')
    nettoyage_more = fields.Text(u'Informations supplémentaires Nettoyage')
    # 3-------------------------------------------------------------------------------------
    # info immeuble
    # abord
    trotoire = fields.Text('Trottoirs')
    mur_mitoyens = fields.Text('Mur mitoyens')
    more_info = fields.Text(u'Informations supplémentaires et observations particulières')

    # facade
    facade_id = fields.One2many('building.facade', 'signalitic_id', string='Facade')
    facade_isolation = fields.Boolean('Isolation')
    facade_repeir_id = fields.One2many('facade.repair', 'signalitic_id', string='Reparation facade')
    # chassis
    chassis_type = fields.Selection([('bois', 'bois'), ('pvc', 'pvc'), ('alu', 'alu')], string='Type de chassis')
    chassis_vitrage = fields.Selection([('simple', 'simple'), ('double', 'double')], string='Vitrage')
    chassis_vitrage_four = fields.Char('Fabricant')
    chassis_color = fields.Char('Couleur')
    chassis_more = fields.Text(u'Informations supplémentaires et observations particulières chassis')
    # terasse
    terasse_ids = fields.One2many('building.terasse', 'signalitic_id', string='Terasse')
    terasse_repeir_ids = fields.One2many('building.repeir.terasse', 'signalitic_id', string='Réparation Terasse')
    

    # parlophone et boite
    plaquette_supplier = fields.Many2one('res.partner', u'Société de plaquettes')
    parlophone_description = fields.Text('Parlophonie: informations et descriptions')
    parlophone_date = fields.Date(u'Dernière mise à jour des plaquettes')
    parlophone_more = fields.Text(u'Informations supplémentaires et observations particulières parlophone')
    boite_bool = fields.Boolean('Plaquettes boites')
    ascenseur_bool = fields.Boolean('Plaquettes ascensseur')
    appartements_bool = fields.Boolean('Plaquettes appartements')
    parlophone_bool = fields.Boolean('Plaquettes parlophone')

    # toiture
    toiture_type = fields.Char('Type de toiture')
    toiture_contract = fields.Char("Contrat d'entretien toiture")
    toiture_obs = fields.One2many('observation.toiture', 'signalitic_id', string='Observation Toiture')
    toiture_isolation = fields.Boolean('Isolation Toiture')
    toiture_repa = fields.One2many('repeir.toiture', 'signalitic_id', string='Observation')

    # jardin
    jardin_contrat = fields.Many2one('res.partner', 'Contrat d\'entretien jardin')
    date_jardin = fields.Date('Date anniversaire du contrat jardin')
    jardin_onservation = fields.One2many('jardin.observation', 'signalitic_id', string='Observation jardin')
    jardin_more = fields.Text(u'Informations supplémentaires Jardin')

    # ascensseur
    ascensseur_contrat = fields.Many2one('res.partner', 'Contrat d\'entretien ascensseur')
    ascensseur_date = fields.Date('Date anniversaire du contrat ascensseur')
    nbr_passage = fields.Integer('Nombre de passage par an')
    ascensseur_ids = fields.One2many('ascensseurs', 'signalitic_id', string='Ascenseurs')
    repeir_ascensseur_ids = fields.One2many('repeir.ascensseur', 'signalitic_id', string=u'Réparation ascensseur')
    cylindre_bool = fields.Boolean('cylindre')
    entr_control = fields.Many2one('res.partner', u'Société de contrôle')
    ascensseur_more = fields.Text(u'Observation complémentaires')

    # compteur
    societe_compteur = fields.Many2one('res.partner', u'Société')
    date_compteur = fields.Selection(
        [('janvier', 'Janvier'), ('fevrier', 'Fevrier'), ('mars', 'Mars'), ('avril', 'Avril'), ('mai', 'Mai'),
         ('juin', 'Juin'), ('juillet', 'Juillet'), ('aout', 'Aout'), ('septembre', 'Septembre'),
         ('octobre', 'Octobre'), ('novembre', 'Novembre'), ('decembre', 'Decembre')], 'mois')
    date_contrat_compteur = fields.Date('Date anniversaire du contrat compteur')

    # chauffage
    chauffage_type = fields.Selection([('individuel', 'Individuel'),
                                       ('collectif', 'Collectif')], 'Type de chauffage')
    eau_chaude_type = fields.Selection([('individuel', 'Individuel'),
                                        ('collectif', 'Collectif')], 'Production eau chaude')
    type_chauffage = fields.Selection([('gaz', 'Gaz'),
                                       ('mazoutb', 'Mazout type b'),
                                       ('mazoutc', 'Mazout type c')], 'Type de chauffage(Mazout,gaz)')
    condensation_chauffage = fields.Boolean(u'A condensation ')
    type_chauffages = fields.Char('Autre type')
    situation_chauffage = fields.Text('Situation')
    nbr_chaudiere = fields.Integer('Nombre de chaudiere')
    chauffage_cascade = fields.Boolean(u'Chaudière en cascade')
    contrat_chaudiere = fields.Many2one('res.partner', 'Contrat d\'entretien chaudiere')
    chaudiere_entretien_date = fields.Date('Date anniversaire d\'entretien chaudiere')
    chaudiere_omnium = fields.Boolean('Contrat omnium')
    chaudiere_tubage = fields.Boolean(u'Tubage de la cheminée')
    chaudiere_separboue = fields.Boolean(u'Séparateur de boues')
    chaudiere_horloge = fields.Boolean('Horloge')
    piece_chaudiere_ids = fields.One2many('piece.chauffage', 'signalitic_id', string=u'Pièce chauffage')
    descr_regul = fields.Text(u'Description de la régulation')
    repeir_chaudiere_ids = fields.One2many('repeir.chaudiere', 'signalitic_id', string=u'Réparation chaudière')
    chaudiere_more = fields.Text(u'Observation complémentaire')

    # adoussisseur
    type_adoucisseur = fields.Char('Type d adoucisseur')
    marque_adoucisseur = fields.Char('Marque adoucisseur')
    numeros_adoucisseur = fields.Char('Numeros adoucisseur')
    annee_adoucisseur = fields.Integer(u'Année de construction')
    supplier_adoucisseur = fields.Many2one('res.partner', 'Contrat d\'entretien adoucisseur')
    qte_adoucisseur = fields.Integer(u'Quantité généralement commandées')
    adoucisseur_more = fields.Text('Observations')

    # Citerne
    marque_citerne = fields.Char('Marque')
    type_citerne = fields.Char('Type de citerne')
    annee_citerne = fields.Date(u'Date du contrôle')
    qte_citerne = fields.Integer(u'Capacité de la citerne')

    # egoutage
    egoutage_contrat = fields.Many2one('res.partner', 'Contrat d\'entretien egoutage')
    egoutage_contrat_date = fields.Date('Date anniversaire du contrat egoutage')
    obs_egoutage_ids = fields.One2many('egoutage.observation', 'signalitic_id', string=u"Réparations egoutages")
    egoutage_more = fields.Text(u"Informations supplémentaires et observations particulières egoutage")

    # extincteur
    extincteur_ids = fields.One2many('extincteur', 'signalitic_id', 'Extincteurs')
    extincteur_more = fields.Text(u'observations particulières')

    # instal elec
    elec_contrat = fields.Many2one('res.partner', 'Contrat d\'entretien electricité')
    elec_building = fields.Many2one('res.partner', u'electricien du bâtiment')
    elec_releve_by = fields.Char(u'Relevé par')

    # garage
    garage_contrat = fields.Many2one('res.partner', 'Contrat d\'entretien garage')
    garage_contrat_date = fields.Date('date anniversaire du contrat garage')
    garage_repeir_ids = fields.One2many('repeir.garage', 'signalitic_id', string=u'Réparation garage')
    garage_description = fields.Text(u'Observations complémentaires')

    # travaux
    travaux_ids = fields.One2many('repeir.general', 'signalitic_id', string='Travaux')
