# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Deduplicate(models.TransientModel):
    _name = 'syndic.tools.deduplicate'

    model_id = fields.Many2one('ir.model', 'Model')
    name_research = fields.Char('Nom cherché')
    id_master = fields.Char('ID master')
    duplicate_ids = fields.One2many('syndic.tools.deduplicate.rec', 'deduplicate_id', 'Record Duplicqué')
    deduplicate_ids = fields.One2many('syndic.tools.deduplicate.model', 'deduplicate_id', 'Modeles')

    @api.one
    def search_occurance(self):
        for duplicate_rec in self.env[self.model_id.name].search([('name', 'ilike', self.name_research)]):
            vals = {
                'name': duplicate_rec.name,
                'rec_id': duplicate_rec.id,
                'deduplicate_id': self.id,
            }
            self.env['syndic.tools.deduplicate.rec'].create(vals)

    @api.one
    def deduplicate(self):
        move_ids = [duplicate_id.id for duplicate_id in self.duplicate_ids]

        for deduplicate_id in self.deduplicate_ids:
            import ipdb;ipdb.set_trace()
            move = self.env[deduplicate_id.model_id.name].search([(deduplicate_id.champs, 'in', move_ids)])
            print move_ids
            move.write({deduplicate_id.champs: self.id_master})
            print 'write -- %s -- %s --> model: %s' % (deduplicate_id.champs, self.id_master, move._name)

        del_ids = set(move_ids) - set([self.id_master])
        self.env[self.model_id.name].browse(del_ids).unlink()


class DeduplicateModel(models.TransientModel):
    _name = 'syndic.tools.deduplicate.model'

    model_id = fields.Many2one('ir.model', 'Model')
    champs = fields.Char('columns')
    deduplicate_id = fields.Many2one('syndic.tools.deduplicate', 'Models')


class DeduplicateRec(models.TransientModel):
    _name = 'syndic.tools.deduplicate.rec'

    name = fields.Char('Nom')
    rec_id = fields.Char('ID')
    deduplicate_id = fields.Many2one('syndic.tools.deduplicate', 'Models')
