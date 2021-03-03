odoo.define('timeline.dashboard', function (require) {
"use strict";

const AbstractAction = require('web.AbstractAction');
const { actionRegistry } = require('web.core');
var core = require('web.core');
const { ComponentWrapper, WidgetAdapterMixin} = require('web.OwlCompatibility');
const { Component, useState, mount } = owl;
const { xml } = owl.tags;

class Cell extends Component {
    static template = xml`
        <div id="2021 - Janvier" class="col-12" style="text-align: center;">
            <h2 class="header-month"><t t-esc="props.month"/></h2>
        </div>
    `;
    
    state = useState({
        year: 2020,
        month: 'Janvier',
    });
}

class App extends Component {
    constructor() {
        super(...arguments);
        var self = this
        this.rpc({route: '/timeline/statistics'}).then(function (months) {
            self.state.months = months.myEvents;
            console.log(self.state.months)
        });
    }

    static template = xml`
    <div class="col-lg-2">
        <div class="row month">
            <t t-foreach="state.months" t-as="month">
                <Cell month="month.date" t-key="month.month"/>
            </t>
        </div>
    </div>`;

    state = useState({
        months: []
    });

    static components = { Cell };
}


const ClientAction = AbstractAction.extend(WidgetAdapterMixin, { 
    start() { 
        const component = new ComponentWrapper(this, App);
        return component.mount( this.el.querySelector('.o_content') 
    ); }, 
}); 


core.action_registry.add('timeline.dashboard', ClientAction);

});
