from odoo import models, fields, api

from datetime import date

class BarcodeImport(models.AbstractModel):
    _name = 'barcode.import'
    _description = 'Mixin for barcode importation'

    _building_field = 'immeuble_id'
    _barcode_type = False

    code = fields.Char('Code', readonly=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Pieces Jointes')

    def _auto_init(self):
        def table_exists(cr, table):
            cr.execute(
                """
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_name = %s
                    AND table_type = 'BASE TABLE'
            """,
                [table],
            )
            return cr.fetchone() 

        if self._name != 'barcode.import':
            # create column when init the model
            if table_exists(self.env.cr, self._table):
                self.env.cr.execute("""ALTER TABLE "%s" ADD COLUMN IF NOT EXISTS "code" varchar""" % (self._table))

            # create new sequence
            buildings = self.env['syndic.building'].search(['|', ('active', '=', False), ('active', '=', True)])
            for building in buildings:
                name = 'barcode-import-%s-%s' % (self._barcode_type, building.name) 
                if not self.env['ir.sequence'].search([
                    ('name', '=', name),
                    ('code', '=', name)
                ]):
                    self.env['ir.sequence'].create({
                        'name': name,
                        'code': name,
                        'padding': 3,
                    })

            # create sequence for old datas
            if table_exists(self.env.cr, self._table):
                no_codes = self.search([('code', '=', False)])
                for no_code in no_codes:
                    buillding = no_code._get_building()
                    new_code = 'barcode-import-%s-%s' % (self._name, buillding.name)
                    seq = self.env['ir.sequence'].next_by_code(new_code)
                    no_code.write({
                        'code': self._get_sequence(buillding, self._barcode_type, seq)
                    })

            # create report
            name = 'Barcode-%s Report' % (self._name)
            if not self.env['ir.actions.report'].search([('name', '=', name)]):
                self.env['ir.actions.report'].create({
                    'name': name,
                    'model': self._name,
                    'report_type': 'qweb-pdf',
                    'report_name': 'syndic_tools.barcode_default',
                    'paperformat_id': self.env.ref('syndic_tools.barcode_paperformat').id,
                    'binding_model_id': self.env['ir.model'].search([('model', '=', self._name)], limit=1).id
                })

        return super(BarcodeImport, self)._auto_init()

    def _get_building(self):
        return self if self._name =='syndic.building' else self[self._building_field]

    def _get_sequence(self, building, type_seq, sequence):
        return '%03d-%s%s-%s' % (building.num_building, date.today().year, type_seq, sequence)

    @api.model
    def create(self, vals):
        rec = super(BarcodeImport, self).create(vals)
        if self._name == 'syndic.building':
            for model_name in self.env.registry.models:
                model = self.env.registry.models[model_name]
                inherit = model._inherit
                if isinstance(inherit, list) and 'barcode.import' in inherit or isinstance(inherit, str) and 'barcode.import' == inherit:
                    name = 'barcode-import-%s-%s' % (model._name, rec.name)
                    self.env['ir.sequence'].create({
                        'name': name,
                        'code': name,
                        'padding': 3,
                    })
        else:
            seq = self.env['ir.sequence'].next_by_code(
                'barcode-import-%s-%s' % (self._barcode_type, rec._get_building().name)
            )
            rec.code = self._get_sequence(
                rec._get_building(),
                self._barcode_type,
                seq
            )
        return rec

    def write(self, vals):
        if vals.get(self._building_field):
            building = self.env['syndic.building'].browse(vals[self._building_field])
            seq = self.env['ir.sequence'].next_by_code(
                'barcode-import-%s-%s' % (self._barcode_type, building.name)
            )
            vals['code'] = self._get_sequence(
                building,
                self._barcode_type,
                seq
            )
        return super(BarcodeImport, self).write(vals)

    def barcode_import(self):
        self.ensure_one()
        return {
            'name': 'Barcode import',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'barecode.importation',
            'type': 'ir.actions.act_window',
            'context': self._context,
            'target': 'new',
        }
