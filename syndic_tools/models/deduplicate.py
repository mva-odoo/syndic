# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Deduplicate(models.Model):
    _name = 'syndic.tools.deduplicate'
    _rec_name = 'name_research'

    model_id = fields.Many2one('ir.model', 'Model')
    name_research = fields.Char(u'Nom cherché')
    name_translate = fields.Char('Nom traduit')
    id_master = fields.Char('ID master')
    duplicate_ids = fields.One2many('syndic.tools.deduplicate.rec', 'deduplicate_id', u'Record Duplicqué')

    @api.one
    def search_occurance(self):
        if self.env.uid == 1:
            self.duplicate_ids = False
            for duplicate_rec in self.env[self.model_id.name].search([
                '|',
                ('name', '=like', self.name_research),
                ('name', 'ilike', self.name_translate)
            ]):
                vals = {
                    'name': duplicate_rec.name,
                    'rec_id': duplicate_rec.id,
                    'deduplicate_id': self.id,
                }
                self.env['syndic.tools.deduplicate.rec'].create(vals)

    @api.one
    def _get_fk_on(self, table):
        q = """  SELECT cl1.relname as table,
                        att1.attname as column
                   FROM pg_constraint as con, pg_class as cl1, pg_class as cl2,
                        pg_attribute as att1, pg_attribute as att2
                  WHERE con.conrelid = cl1.oid
                    AND con.confrelid = cl2.oid
                    AND array_lower(con.conkey, 1) = 1
                    AND con.conkey[1] = att1.attnum
                    AND att1.attrelid = cl1.oid
                    AND cl2.relname = %s
                    AND att2.attname = 'id'
                    AND array_lower(con.confkey, 1) = 1
                    AND con.confkey[1] = att2.attnum
                    AND att2.attrelid = cl2.oid
                    AND con.contype = 'f'
        """
        return self.env.cr.execute(q, (table,))

    @api.one
    def deduplicate(self):
        if self.env.uid == 1:
            slave_ids = set(self.duplicate_ids.mapped('rec_id')) - set([self.id_master])
            model_name = self.model_id.name.replace('.', '_')
            self._get_fk_on(model_name)

            for table, column in self.env.cr.fetchall():
                dupl_ids = [int(dupl_id) for dupl_id in self.duplicate_ids.mapped('rec_id')]
                datas_ids = self.env[table.replace('_', '.')].search([(column, 'in', dupl_ids)]).ids
                if datas_ids:
                    if len(tuple(datas_ids)) > 1:
                        update_query = "UPDATE "+table+" SET "+column+"="+self.id_master+" WHERE id IN "+str(tuple(datas_ids))
                    else:
                        update_query = "UPDATE "+table+" SET "+column+"="+self.id_master+" WHERE id = "+str(tuple(datas_ids)[0])
                    self.env.cr.execute(update_query, ())

                self.env[self.model_id.name].search([('id', 'in', tuple(slave_ids))]).unlink()


class DeduplicateRec(models.Model):
    _name = 'syndic.tools.deduplicate.rec'

    name = fields.Char('Nom')
    rec_id = fields.Char('ID')
    deduplicate_id = fields.Many2one('syndic.tools.deduplicate', 'Models')
