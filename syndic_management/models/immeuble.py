# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from xlwt import Workbook
import StringIO
import base64


class ExportFicheTech(models.TransientModel):
    _name ='export.fiche.tech'

    xls_file = fields.Binary("cliquez ici", readonly=True, default='_get_export_fiche_technique')
    datas_fname = fields.Char("Fichier", readonly=True, default='export.xls')

    @api.model
    def _get_export_fiche_technique(self):
        if self._context:
            active_id = self._context.get('active_id')
            xls = Workbook()
            # sheet 1 creation
            feuil1 = xls.add_sheet('sheet 1')

            # add header
            row = 0
            feuil1.write(row, 0, 'Nom du fournisseur')
            feuil1.write(row, 1, 'Metier')
            feuil1.write(row, 2, 'Adresse')
            feuil1.write(row, 3, 'Ville')
            feuil1.write(row, 4, 'Code Postal')
            feuil1.write(row, 5, 'Pays')
            feuil1.write(row, 6, 'Telephone')
            feuil1.write(row, 7, 'Email')

            for fournisseur_id in self.env['syndic.building'].search([('id', '=', active_id)]).supplier_ids:
                row += 1
                metier_ids = ','.join([job_id.name for job_id in fournisseur_id.job_ids])

                feuil1.write(row, 0, fournisseur_id.name)
                feuil1.write(row, 1, metier_ids)
                feuil1.write(row, 2, fournisseur_id.street)
                feuil1.write(row, 3, fournisseur_id.city_id.name)
                feuil1.write(row, 4, fournisseur_id.zip)
                feuil1.write(row, 5, fournisseur_id.country_id.name)
                feuil1.write(row, 6, fournisseur_id.phone)
                feuil1.write(row, 7, fournisseur_id.email)

            output = StringIO.StringIO()
            xls.save(output)
            encode_text = base64.encodestring(output.getvalue())

            return encode_text


class Building(models.Model):
    _name = 'syndic.building'
    _order = 'name asc'

    @api.one
    def _get_total_quotites(self):
        total_quotites = 0.00
        for lot in self.lot_ids:
            total_quotites += lot.quotities
        self.total_quotites = total_quotites

    name = fields.Char('Immeuble', required=True)
    lot_ids = fields.One2many('syndic.lot', 'building_id', 'Lots')
    BCE = fields.Char('BCE')
    num_building = fields.Integer("N°", required=True)
    address_building = fields.Char('Adresse', required=True)
    zip_building = fields.Integer('Code Postal', required=True)
    city_building = fields.Many2one('city', 'Commune', required=True)
    supplier_ids = fields.Many2many('syndic.supplier', string="Fiche technique")
    compte = fields.Char('Compte en banque')
    total_quotites = fields.Float(compute=_get_total_quotites, string='Total Quotites')
    active = fields.Boolean(default=True)

    @api.multi
    def go_export_model(self):
        return {
            'name': 'Export ficher technique',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'export.fiche.tech',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': self._context,
        }

