from odoo import models, fields, api


class BarcodeImport(models.AbstractModel):
    _name = 'barcode.import'
    _description = 'Mixin for barcode importation'

    _building_field = 'immeuble_id'
    _barcode_type = '001'

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
                name = 'barcode-import-%s-%s' % (self._name, building.name) 
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
                        'code': self._get_sequence(self._barcode_type, buillding.name, seq)
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
        return self[self._building_field]

    def _get_sequence(self, seq_type, building_name, sequence):
        return '%s-%s-%s' % (seq_type, building_name, sequence)

    @api.model
    def create(self, vals):
        rec = super(BarcodeImport, self).create(vals)
        seq = self.env['ir.sequence'].next_by_code(
            'barcode-import-%s-%s' % (self._name, rec._get_building().name)
        )
        rec.code = self._get_sequence(self._barcode_type, rec._get_building().name, seq)
        return rec

    def write(self, vals):
        if vals.get(self._building_field):
            building_name = self.env['syndic.building'].browse(vals[self._building_field]).name
            seq = self.env['ir.sequence'].next_by_code(
                'barcode-import-%s-%s' % (self._name, building_name)
            )
            vals['code'] = self._get_sequence(
                self._barcode_type,
                building_name,
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
