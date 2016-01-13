openerp.pdf_viewer = function(instance, local) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    local.HomePage = instance.Widget.extend({
        template: "PDFViewer",
        init: function(parent, action) {
            this._super(parent);
            this.url = '';
            debugger;
            this.report = action.context['report'];
            if ((typeof action.context['report'] !== "undefined") && (typeof action.context['active_id'] !== "undefined")){
                if (typeof action.context['active_ids'] !== "undefined"){
                    this.url = '/report/pdf/'+action.context['report']+'/'+action.context['active_ids'];
                }
                else{
                   this.url = '/report/pdf/'+action.context['report']+'/'+action.context['active_id'];
                }
            }
        },
    });

    instance.web.client_actions.add('pdf_viewer.homepage', 'instance.pdf_viewer.HomePage');
}


odoo.define('sgimmo.custom_report', function (require) {
    var ActionManager = require('web.ActionManager');
    var core = require('web.core');
    var crash_manager = require('web.crash_manager');
    var framework = require('web.framework');
    var session = require('web.session');
    var pyeval = require('web.pyeval');

     ActionManager.include({
        ir_actions_report_xml: function(action, options) {
            var self = this;
            framework.blockUI();
            action = _.clone(action);
            var eval_contexts = ([session.user_context] || []).concat([action.context]);

            _t =  core._t;
            new_action = {
                'tag': 'pdf_viewer.homepage',
                'name': 'pdf_viewer',
                'type': "ir.actions.client",
            };

            new_action.context = pyeval.eval('contexts',eval_contexts);
            new_action.context['report'] = action['report_name']

            return $.Deferred(function (d) {
                $.when(self.ir_actions_client(new_action,options)).then(function () {
                    framework.unblockUI();
                    d.resolve();
                });

            });


        }
    });
});


