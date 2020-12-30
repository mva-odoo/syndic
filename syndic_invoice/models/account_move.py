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
