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
        <div id="test1" style="text-align: center;">
            <t t-foreach="props.first" t-as="first_building">
                <div>
                    <t t-esc="first_building"/>
                </div>    
            </t>
            <hr/>
            <t t-foreach="props.last" t-as="last_building">
                <div>
                    <t t-esc="last_building"/>
                </div>    
            </t>
        </div>
    `;
}


class Month extends Component {
    static template = xml`
        <div id="2021 - Janvier" class="col-12" style="text-align: center;">
            <h2 class="header-month"><t t-esc="props.month"/></h2>
            <Cell month="props.month" first="props.first" last="props.last"/>
        </div>
    `;
    
    static components = { Cell }
}


let getMonth = function(datas, month_int){
    let new_vals = {};

            var d = new Date();
            var n = d.getMonth();

            // var month_int = [-1, 0, 1, 2, 3, 4]
            
            for (let selected_month of month_int){
                let d = new Date();
                d.setMonth(d.getMonth() + selected_month);

                let i = d.getMonth()
                new_vals[i] = datas[i]
            }

            return new_vals
}

class App extends Component {
    constructor() {
        super(...arguments);
        var self = this
        this.rpc({route: '/ag/months'}).then(function (months) {
            self.state.allMonths = months;
            self.state.months = getMonth(self.state.allMonths, [-1, 0, 1, 2, 3, 4])
        });
    }

    static template = xml`
    <div class="dashboard-content">
        <div class="row dashboard-header">
            <span t-on-click="changeMonth">Hello</span>
        </div>
        <div class="row month">
            <t t-foreach="state.months" t-as="month">
                <div class="col-2">
                    <Month month="month_value.name" first="month_value.first" last="month_value.last" t-key="month"/>
                </div>
            </t>
        </div>
    </div>`;

    state = useState({
        months: []
    });

    static components = { Month };


    changeMonth(ev) {
        var self = this
        self.state.months = getMonth(self.state.allMonths, [-1, 0, 1, 2, 3, 5])
    }
}


const ClientAction = AbstractAction.extend(WidgetAdapterMixin, { 
    start() { 
        const component = new ComponentWrapper(this, App);
        return component.mount( this.el.querySelector('.o_content') 
    ); }, 
}); 


core.action_registry.add('timeline.dashboard', ClientAction);

});
