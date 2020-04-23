odoo.define('sgimmo.custom_calendar', function (require) {
    var CalendarView = require('web.CalendarRenderer');
    var self = this;

    CalendarView.include({

      _initCalendar: function () {
        fc_options = this.state.fc_options;
        fc_options['weekends'] = false;
        fc_options['axisFormat'] = 'H(:mm)';
        // fc_options['minTime'] = 7;
        // fc_options['maxTime'] = 20;
        this._super.apply(this, arguments);
      },
    });
});
