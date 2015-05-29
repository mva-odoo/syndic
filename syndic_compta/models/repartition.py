# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
import datetime

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