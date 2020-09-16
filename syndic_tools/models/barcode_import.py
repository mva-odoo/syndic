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

    def _get_sequence(self, building):
        name = 'barcode-import-%s-%s' % (self._barcode_type, building.name) 
        sequence = self.env['ir.sequence'].search([
            ('name', '=', name),
            ('code', '=', name)
        ], limit=1)

        if not sequence:
            return self.env['ir.sequence'].sudo().create({
                'name': name,
                'code': name,
                'padding': 3,
            })

        return sequence

    def _get_report(self):
        if self._print_barcode:
            key_name = '%s_report_view' % (self._table)
            if not self.env['ir.ui.view'].search([
                ('name', '=', key_name),
                ('key', '=', 'barcode_import.%s' % key_name),
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

    @api.model
    def create(self, vals):
        rec = super(BarcodeImport, self).create(vals)

        building = rec[rec._building_field] if rec._building_field != 'id' else rec

        sequence = rec.sudo()._get_sequence(building)
        rec.sudo()._get_report()
        seq = self.env['ir.sequence'].next_by_code(
            sequence.code
        )

        rec.code = "%03d-%s%s-%s" % (
            building.num_building,
            self._barcode_type,
            date.today().year,
            seq
        )
        return rec

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
