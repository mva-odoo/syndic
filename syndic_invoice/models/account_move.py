# -*- coding: utf-8 -*-

from odoo import api, fields, models
import requests

class AccountMove(models.Model):
    _inherit = 'account.move'

    building_id = fields.Many2one('syndic.building', 'Immeuble')
    sogis_ref = fields.Char('Sogis ref.')
    sogis_trimestre = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ], string='Trimestre')

    def _call_sogis(self, method, *args, **kwarks):
        URL = self.env['ir.config_parameter'].sudo().get_param('sogis_url')

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'login': self.env['ir.config_parameter'].sudo().get_param('sogis_login'),
            'password': self.env['ir.config_parameter'].sudo().get_param('sogis_password'),
        }
        response = requests.post(
            URL+method,
            headers=headers,
            data=kwarks
        )
        resp = response.json()
        if resp.get('error'):
            raise Warning(resp['error'])
        return resp.get('data')

    def _get_building(self, num_building):
        datas = self._call_sogis('/api/getCoproprietes')
        for data in datas:
            if int(data['num_copropriete']) == num_building:
                return data['id_copropriete']

    def upload_sogis(self):
        for rec in self:
            params = {}
            params['id_fournisseur'] = '618'
            params['id_facture'] = '999999999998'
            params['id_copropriete'] = self._get_building(rec.building_id.num_building)
            params['ref_facture'] = rec.name
            params['trimestre'] = rec.sogis_trimestre
            # params['com_vcs'] = rec.invoice_payment_ref
            params['id_cle'] = '23'
            params['classe_compta'] = '61300'
            params['id_pcmn'] = '17467'
            params['montant_ht'] = str(rec.amount_untaxed)
            params['montant_tva'] = str(rec.amount_tax)
            # params['update'] = '1'
            params['tva_valeur'] = '21'
            # params['montant_ttc'] = str(rec.amount_total)
            params['date_facture'] = fields.datetime.to_string(rec.invoice_date)
            # params['nom_fichier'] = 
            # params['fichier_facture'] = 

            datas = self._call_sogis('/api/insertUpdateFacture', params)

            rec.sogis_ref = datas.get('ref_interne')
