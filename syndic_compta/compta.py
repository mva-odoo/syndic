# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions

class Facture(models.Model):
    _name = 'syndic.facture'
    name = fields.Char('Facture numeros')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble', required=True)
    invoice_date = fields.Date('Date de facture', required=True)
    facture_line_ids = fields.One2many('syndic.facture.ligne', 'facture_id', 'Ligne de facture')
    state = fields.Selection([('draft', 'Brouillon'), ('validate', 'Validé'), ('close', 'Fermé')],
                             'Etat', default='draft')
    facture_detail_ids = fields.One2many('syndic.facture.detail', 'facture_id', 'Detail de facture')

    @api.one
    def validate_facture(self):
        if self.state != 'validate':
            for line in self.facture_line_ids:
                check_amount = 0.00
                for repartition_line in line.repartition_lot_id.repart_detail_ids:
                    amount = line.amount * (repartition_line.value/1000)
                    proprio_id = False
                    if repartition_line.lot_id.proprio_id:
                        proprio_id = repartition_line.lot_id.proprio_id.id
                    self.env['syndic.facture.detail'].create({
                        'facture_id': self.id,
                        'facture_line_id': line.id,
                        'aumout': amount,
                        'lot_id': repartition_line.lot_id.id,
                        'account_id': line.account_id.id,
                        'proprietaire_id': proprio_id,
                        'fournisseur_id': line.fournisseur_id.id,
                        })
                    check_amount += amount
                if check_amount != line.amount:
                    raise exceptions.Warning("La totalité de la somme n'a pas été facturé. "
                                             "Vérifié la répartition des quotités")

            self.state = 'validate'

    @api.one
    def reset_draft(self):
        self.facture_detail_ids.unlink()
        self.state = 'draft'

    @api.model
    def create(self, vals):
        new_id = super(Facture, self).create(vals)
        building = self.env['syndic.building'].search([('id', '=', vals['immeuble_id'])])
        new_id.name = '%s/%i' %(building.name, new_id)
        return new_id


class FactureLigne(models.Model):
    _name = 'syndic.facture.ligne'

    name = fields.Char('Description', required=True)
    amount = fields.Float('Montant', required=True)
    invoice_line_date = fields.Date('Date d\'echéhance', required=True)
    fournisseur_id = fields.Many2one('syndic.supplier', 'Fournisseur', required=True)
    account_id = fields.Many2one('syndic.pcmn', 'Compte', required=True)
    repartition_lot_id = fields.Many2one('syndic.repartition.lot', 'Répartition des Lots', required=True)
    facture_id = fields.Many2one('syndic.facture', 'Facture')


class FactureDetail(models.Model):
    _name = 'syndic.facture.detail'
    facture_id = fields.Many2one('syndic.facture', 'origine facture', required=True)
    facture_line_id = fields.Many2one('syndic.facture.ligne', 'origine ligne', required=True)
    aumout = fields.Float('Montant', required=True)
    lot_id = fields.Many2one('syndic.lot', 'Lot')
    account_id = fields.Many2one('syndic.pcmn', 'Compte', required=True)
    proprietaire_id = fields.Many2one('syndic.owner', 'Propriétaire')
    fournisseur_id = fields.Many2one('syndic.supplier', 'Propriétaire')

class Pcmn(models.Model):
    _name = 'syndic.pcmn'
    _rec_name = 'code'
    name = fields.Char('Nom du compte', required=True)
    code = fields.Char('Code du compte', required=True)


class RepartitionLot(models.Model):
    _name = 'syndic.repartition.lot'
    name = fields.Char('Description', required=True)
    repart_detail_ids = fields.One2many('syndic.repartition.lot.detail', 'repartition_id', 'Detail de repartition')
    percentage_lot = fields.Float('Pourcentage des quotités', compute='compute_percentage_quot')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')

    @api.one
    def compute_percentage_quot(self):
        amount = 0.00
        for detail in self.repart_detail_ids:
            amount += detail.value
        self.percentage_lot = amount/10

    @api.one
    def create_normal_repartition(self):
        if not self.repart_detail_ids:
            for lot in self.immeuble_id.lot_ids:
                self.env['syndic.repartition.lot.detail'].create({
                    'lot_id': lot.id,
                    'value': lot.quotities,
                    'repartition_id': self.id,
                })
        else:
            raise exceptions.Warning('Il y a déjà des quotités.')

class RepartitionLotDetail(models.Model):
    _name = 'syndic.repartition.lot.detail'
    _rec_name = 'lot_id'
    repartition_id = fields.Many2one('syndic.repartition.lot', 'Repartition Lot')
    value = fields.Float('Valeur')
    lot_id = fields.Many2one('syndic.lot', 'Lots')

