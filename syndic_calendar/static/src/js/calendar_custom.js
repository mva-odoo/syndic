odoo.define('sgimmo.custom_calendar', function (require) {
    var CalendarView = require('web_calendar.CalendarView');
    CalendarView.include({
        get_fc_init_options: function() {
        options = this._super(parent);
        options['axisFormat'] = 'H(:mm)';
        options['weekends'] = false;
        options['minTime'] = 7;
        options['maxTime'] = 20;
        return options;
        }

    });
});