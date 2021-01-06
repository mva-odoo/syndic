odoo.define('odoo.pdf_viewer', function (require) {
  'use strict';

  var AbstractAction = require('web.AbstractAction');
  var core = require('web.core');
  var framework = require('web.framework');
  var ActionManager = require('web.ActionManager');

  var _t = core._t;

  var Dashboard = AbstractAction.extend({
      contentTemplate: 'PDFViewer',
      hasControlPanel: true,
      
      init: function(parent, action, options) {
        this._super(parent, action, options);

        this._title = _t('Lettre');
        this.url = '';
        var context = action.context;
        
        if ((typeof context.report !== "undefined") && (typeof context.active_id !== "undefined")){
          if (typeof context.active_ids !== "undefined"){
            this.url = '/report/pdf/'+context.report+'/'+context.active_ids;
          }
          else{
            this.url = '/report/pdf/'+context.report+'/'+context.active_id;
          }
        }
          if ((typeof context.multi_report !== "undefined") && (typeof context.active_id !== "undefined")){
            this.url = 'multi_report/'+context.multi_report+'/'+context.active_id+'/'+context.active_model;
            
          }
      },
      start: function(){
            var superDef = this._super.apply(this, arguments);
            return superDef.then(this._updateControlPanel());
      },

      do_show: function () {
          this._super.apply(this, arguments);
          this._updateControlPanel();
      },

      _updateControlPanel: function () {
          // this.updateControlPanel();
      },

  });

  core.action_registry.add('pdf_viewer.homepage', Dashboard);

  var ActionManager = ActionManager.include({
    _triggerDownload: function (action, options, type){
      framework.blockUI();

      var context = action.context;
      if (context.reports !== undefined){
        context.multi_report = context;
      }
      context.report = action.report_name;
      return this.do_action( {
        'tag': 'pdf_viewer.homepage',
        'name': 'pdf_viewer',
        'type': "ir.actions.client",
        'context': context,
      }, options).then(function(){
        framework.unblockUI();
      });
    },
  });
  return Dashboard;
});