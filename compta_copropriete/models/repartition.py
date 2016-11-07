# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Repartition(models.Model):
    _name = 'syndic.compta.repartition'

    name = fields.Char('Description', required=True)
    repart_detail_ids = fields.One2many('syndic.compta.repartition.ligne', 'repartition_id', 'Detail de repartition')
    percentage_lot = fields.Float('Pourcentage des quotités')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')

    @api.one
    def create_normal_repartition(self):
        if not self.repart_detail_ids:
            for lot in self.immeuble_id.lot_ids:
                self.env['syndic.compta.repartition.ligne'].create({
                    'lot_id': lot.id,
                    'value': lot.quotities,
                    'repartition_id': self.id,
                })
        else:
            raise exceptions.Warning('Il y a déjà des quotités.')


class RepartitionLotDetail(models.Model):
    _name = 'syndic.compta.repartition.ligne'
    _rec_name = 'lot_id'

    repartition_id = fields.Many2one('syndic.repartition.lot', 'Repartition Lot')
    value = fields.Float('Valeur')
    lot_id = fields.Many2one('syndic.lot', 'Lots')
