openerp.pdf_viewer = function(instance, local) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;


    local.HomePage = instance.Widget.extend({
        template: "PDFViewer",
        start: function() {
            console.log("load pdf viewer");
        },
        init: function(parent, action) {
            debugger;
            this._super(parent);
            this.report = action.context['report']
            this.url = '/report/pdf/'+action.context['report']+'/'+action.context['active_id'];
        },
    });


    instance.web.client_actions.add('pdf_viewer.homepage', 'instance.pdf_viewer.HomePage');
}