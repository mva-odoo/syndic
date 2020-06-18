from odoo import models, fields, api

from datetime import date


class BarcodeImport(models.AbstractModel):
    _name = 'barcode.import'
    _description = 'Mixin for barcode importation'

    _building_field = 'immeuble_id'
    _barcode_type = False
    _print_barcode = True

    code = fields.Char('Code', readonly=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Pieces Jointes')

    def _default_bracode_view(self, key_view):
        return """
<t t-name='%s'>
    <t t-set="web_url" t-value="docs.env['ir.config_parameter'].sudo().get_param('web.base.url', default='')"/>
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="o">
            <div class="page">
                <div class="barcode" style="max-height:50pt;max-width:100%%;text-align: center;">
                    <img 
                        alt="barcode"
                        t-if="o.code"
                        t-att-src="'%%s/report/barcode/?type=%%s&amp;value=%%s&amp;width=%%s&amp;height=%%s&amp;humanreadable=1' %% (web_url, 'Code128', o.code, 600, 120)"
                        align="center"
                    />
                </div>
            </div>
        </t>
    </t>
</t>
""" % key_view

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
            buildings = self.env['syndic.building'].search_read(['|', ('active', '=', False), ('active', '=', True)], ['name'])
            for building in buildings:
                name = 'barcode-import-%s-%s' % (self._barcode_type, building['name']) 
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
            if self._print_barcode:
                key_name = '%s_report_view' % (self._table)
                if not self.env['ir.ui.view'].search([
                    ('name', '=', key_name),
                    ('key', '=', key_name),
                ]):
                    self.env['ir.ui.view'].create({
                        'name': key_name,
                        'key': 'barcode_import.%s' % key_name,
                        'type': 'qweb',
                        'mode': 'primary',
                        'arch_base': self._default_bracode_view(key_name),
                    })

                name = 'Barcode %s' % self._barcode_type
                if not self.env['ir.actions.report'].search([('name', '=', name)]):
                    self.env['ir.actions.report'].create({
                        'name': name,
                        'model': self._name,
                        'report_type': 'qweb-pdf',
                        'report_name': 'barcode_import.%s' % key_name,
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
