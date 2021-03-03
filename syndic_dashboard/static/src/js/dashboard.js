odoo.define('timeline.dashboard', function (require) {
"use strict";
var AbstractAction = require('web.AbstractAction');
// var ControlPanelMixin = require('web.ControlPanelMixin');
var core = require('web.core');
var session = require('web.session');

// var App = require('syndic.dashboard.components');
const { Component, useState, mount } = owl;
const { xml } = owl.tags;

var qweb = core.qweb;



class Cell extends Component {
    static template = xml`
        <div id="2021 - Janvier" class="col-12" style="text-align: center;">
            <h2 class="header-month"><t t-esc="props.id"/> --- <t t-esc="state.year"/> - <t t-esc="state.month"/></h2>
        </div>
    `;
    
    state = useState({
        year: 2020,
        month: 'Janvier',
    });

	mounted() {
		this.state.year = 2021
	}

	getData() {
		return 2021
	}

}

class App extends Component {
    static template = xml`
    <div class="col-lg-2">
        <div class="row month">
            <Cell id="10"/>
            <Cell />
        </div>
    </div>`;

    static components = { Cell };
}




// var Dashboard = AbstractAction.extend(ControlPanelMixin, {
var Dashboard = AbstractAction.extend({
	template: 'dashboardTimeline',

	events: {
		'click .building_btn': '_openBuilding',
		'click .calendar_btn': '_openCalendar',
		'click .letter_btn': '_openLetter',
		'click .todo_btn': '_opentodo',
    },

	willStart: function(){
		var self = this;
        var statsDef = this._rpc({route: '/timeline/statistics'}).then(function (stats) {
            self.stats = stats;
        });

		// var buildingsDef = this._rpc({route: '/dashboard/buildings'}).then(function (buildings) {
		// 	self.buildings = buildings;
		// 	self.buildings_len = buildings.buildings.length;
		// });

        var superDef = this._super.apply(this, arguments);

        // return $.when(buildingsDef, statsDef, superDef);
		return Promise.all([
			statsDef,
			superDef
		])
	},

	start: function(){
        var superDef = this._super.apply(this, arguments);
        this._renderButtons();

        return superDef
			.then(this._updateControlPanel())
			// .then(this._render_building.bind(this))
			.then(this._render_meetings.bind(this));
	},

	_render_building: function(){
		var new_this = this;
		new_this.$('.my-buildings').append('<p>Vous Avez '+this.buildings_len+ ' immeubles</p>');
		this.buildings.buildings.forEach(function(values, key) {
			new_this.$('.my-buildings').append('<p><a href="javascript:;" class="building_btn" data-id='+values.id+'>'+values.name+'</a></p>');
		})

	},

	_render_meetings: function(){
		mount(App, { target: document.body });
		var new_this = this;
		this.stats.myEvents.forEach(function(value) {
			var $div2 = $("<div>", {"class": "col-lg-2"});
			var $row = $("<div>", {"class": "row month"});
			var $month = $("<div>", {id: value.date, "class": "col-12"}).css('text-align', 'center');
			
			$month.html('<h2 class="header-month">'+value.date+'</h2>');
			
			$div2.append($row);
			$row.append($month);

			new_this.$('.allmonth').append($div2);
			
			var $body_premier = $("<ul>", {id: "premier"+value.month, "class": "col-md-12"});
			$row.append($body_premier);
				
			value.premier.forEach(function(element) {
				var el_manager = '';
				var date = '';
				if (element.manager_id !== undefined && element.manager_id[0] == session.uid){
					el_manager = 'el_manager'
				}

				var building_name = '<a href="javascript:;" class="building_btn premierli '+el_manager+'" data-id='+element["id"]+'>'+element['name']+'</a> ';
				var calendar_icon = ' <a href="javascript:;" class="calendar_btn '+el_manager+'" data-building_id='+element["id"]+' data-name='+element["name"]+'><i class="fa fa-calendar"></i>';
				var envelope_icon = '</a> <a href="javascript:;" class="letter_btn '+el_manager+'" data-building_id='+element["id"]+'><i class="fa fa-envelope"></i> ';
				
				var date = '';
				if (element['is_set'] !== false){
					date = ' ('+element['is_set']+') ';
				}
				var $building_html = '<li class="premierli '+el_manager+'">'+calendar_icon+envelope_icon+building_name+date+'</li></a>';
				new_this.$("#premier"+value.month).append($building_html);
			});
			
			var $month2 = $("<div>", {id: value.date, "class": "col-12"}).css('text-align', 'center');;
			$month2.html('<h4 class="header-month"> Deuxième Quinzaine</h4>');
			$row.append($month2);

			var $body_deuxieme = $("<ul>", {id: "deuxieme"+value.month, "class": "col-12"});
			$row.append($body_deuxieme);
			
			value.deuxieme.forEach(function(element) {
				var el_manager = '';
				var date = '';
				if (element.manager_id !== undefined && element.manager_id[0] == session.uid){
					el_manager = 'el_manager'
				}
				if (element['is_set'] !== false){
					date = ' ('+element['is_set']+') ';
				}

				var building_name = '<a href="javascript:;" class="building_btn deuxiemeli '+el_manager+'" data-id='+element["id"]+'>'+element['name']+'</a> ';
				var calendar_icon = ' <a href="javascript:;" class="calendar_btn" data-building_id='+element["id"]+' data-name='+element["name"]+'><i class="fa fa-calendar"></i>';
				var envelope_icon = '</a> <a href="javascript:;" class="letter_btn" data-building_id='+element["id"]+'><i class="fa fa-envelope"></i> ';			
				var $building2_html = '<li class="deuxiemeli '+el_manager+'"> '+calendar_icon+envelope_icon+building_name+date+'</li></a>';
	
				new_this.$("#deuxieme"+value.month).append($building2_html);
			});
		});

	},

	_openBuilding: function (event) {
		var building_id = $(event.currentTarget).data('id');

		return this.do_action({
				res_id: building_id,
				name: 'Immeuble',
				res_model: 'syndic.building',
				type: 'ir.actions.act_window',
				views: [[false, 'form']],
		});
	
	},
	_opentodo: function (event){
		return this.do_action({
			name: 'TODO',
			res_model: 'calendar.event',
			type: 'ir.actions.act_window',
			views: [[false, 'form']],
			target: 'new',
	});
	},

	_openCalendar: function (event) {
		var name = $(event.currentTarget).data('name');
		var building_id = $(event.currentTarget).data('building_id');

		var context = {
			default_building_id: building_id,
			default_name: 'AG '+name,
			default_is_ag: true,
		};
		return this.do_action({
				name: 'Calendrier',
				res_model: 'calendar.event',
				type: 'ir.actions.act_window',
				views: [[false, 'calendar']],
				context: context,
		});
	
	},

	_openLetter: function (event) {
		var building_id = $(event.currentTarget).data('building_id');

		var context = {
			default_immeuble_id: building_id,
			default_all_immeuble: true,
		}

		return this.do_action({
				name: 'Letter',
				res_model: 'letter.letter',
				type: 'ir.actions.act_window',
				views: [[false, 'form']],
				context: context,
		});
	
	},
	_get_my_building: function(event) {
		var self = this;
		var statsDef = this._rpc({route: '/timeline/statistics'}).then(function (stats) {
			self.stats.myEvents.pop();
			this._updateControlPanel().then(
				this._render_building.bind(this)).then(
					this._render_meetings.bind(this)
				);
			
	});
	
	},

	do_show: function () {
    	this._super.apply(this, arguments);
    	this._updateControlPanel();
	},

	_renderButtons: function () {
    	this.$buttons = $(qweb.render('timeline.Buttons'));
    	this.$buttons.on('click', '.o_building_btn', this._get_my_building.bind(this));
	},

	_updateControlPanel: function () {
    	// this.update_control_panel({
          // cp_content: {
          //    $buttons: this.$buttons,
          // },
    	// });
	},

});


core.action_registry.add('timeline.dashboard', Dashboard);

return Dashboard;

});
