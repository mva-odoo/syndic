
odoo.define('odoo.pdf_viewer', function (require) {
    'use strict';

    var Widget = require('web.Widget');
    var core = require('web.core');

    var Dashboard = Widget.extend({
        template: 'PDFViewer',
        init: function(parent, action) {

            this._super(parent);
            this.url = '';
            if ((typeof action.params['report'] !== "undefined") && (typeof action.params['active_id'] !== "undefined")){
                if (typeof action.params['active_ids'] !== "undefined"){
                    this.url = '/report/pdf/'+action.params['report']+'/'+action.params['active_ids'];
                }
                else{
                   this.url = '/report/pdf/'+action.params['report']+'/'+action.params['active_id'];
                }
            }
        },

    });

    core.action_registry.add('pdf_viewer.homepage', Dashboard);
});

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

            new_action = {
                'tag': 'pdf_viewer.homepage',
                'name': 'pdf_viewer',
                'type': "ir.actions.client",
                'params': {
                    'report': action['report_name'],
                    'active_id': action.context['active_id'],
                    'active_ids': action.context['active_ids']},
            };

            new_action.context = pyeval.eval('contexts',eval_contexts);
            return $.Deferred(function (d) {
                $.when(self.ir_actions_client(new_action,options)).then(function () {
                    d.resolve();
                    framework.unblockUI();
                });

            });


        }
    });
});


