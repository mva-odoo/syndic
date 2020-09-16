odoo.define('syndic.fields', function (require) {
"use strict";

var basicFields = require('web.basic_fields');
var fieldRegistry = require('web.field_registry');
var fieldRegistry = require('web.field_registry');
    var RawFieldInteger = basicFields.FieldInteger.extend({

        _formatValue: function (value) {            
            return value || null;
        },
    });

fieldRegistry.add('raw-field-integer', RawFieldInteger);

});