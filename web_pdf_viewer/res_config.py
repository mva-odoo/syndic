from openerp.osv import fields, osv


class base_config_settings(osv.osv_memory):
    _inherit = 'base.config.settings'
    _columns = {
        'module_web_pdf_viewer': fields.boolean('Use embedded PDF viewer for documents',
                                              help="""Enable this option will open your documents in an embedded PDF viewer"""),
    }