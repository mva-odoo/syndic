# -*- coding: utf-8 -*-

from odoo import api, fields, models
import requests

class AccountMove(models.Model):
    _inherit = 'account.move'

    building_id = fields.Many2one('syndic.building', 'Immeuble')
    sougis_ref = fields.Char('Sogis ref.')

    def _get_building(self, num_building):
        user = 'sgimmo_api'
        password = 'SG2020'
        URL = 'https://www.sogis-serveur45.com/sgimmo949/syndic/soft'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'login': user,
            'password': password,
        }
        response = requests.post(
            URL+'/api/getCoproprietes',
            headers=headers,
        )

        datas = response.json().get('data')
        for data in datas:
            if int(data['num_copropriete']) == num_building:
                return data['id_copropriete']

    def upload_sogis(self):
        user = 'sgimmo_api'
        password = 'SG2020'
        URL = 'https://www.sogis-serveur45.com/sgimmo949/syndic/soft'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'login': user,
            'password': password,
        }
        params = {}
        from datetime import datetime
        for rec in self:
            params['id_fournisseur'] = '618'
            params['id_copropriete'] = self._get_building(rec.building_id.num_building)
            params['ref_facture'] = rec.name
            params['trimestre'] = '4'
            params['com_vcs'] = rec.invoice_payment_ref
            params['id_cle'] = '9509051'
            params['montant_ttc'] = str(rec.amount_total)
            params['date_facture'] = datetime.strftime(rec.invoice_date, "%Y-%m-%d")
            # params['nom_fichier'] = 
            # params['fichier_facture'] = 
            print(params)
            response = requests.post(
                URL+'/api/insertUpdateFacture',
                headers=headers,
                data=params,
            )
            datas = response.json().get('data')
            print(response.json().get('error'))
            import ipdb; ipdb.set_trace()
            rec.sogis_ref = datas.get('ref_interne')
