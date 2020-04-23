# -*- coding: utf-8 -*-

from odoo import http
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


_Mois_fr = {
            1: 'Janvier',
            2: 'Fevrier',
            3: 'Mars',
            4: 'Avril',
            5: 'Mai',
            6: 'Juin',
            7: 'Juillet',
            8: 'Aout',
            9: 'Septembre',
            10: 'Octobre',
            11: 'Novembre',
            12: 'Decembre',
        }


class OrderRoute(http.Controller):
    def _get_is_set(self, year, month, quinzaine, building_id):
        start = datetime(year, month.month, 1)
        end = datetime(year, month.month, 15)
        if quinzaine == 2:
            start = datetime(year, month.month, 15)
            next_month = datetime(year, month.month, 28) + timedelta(days=4)
            end = next_month - timedelta(days=next_month.day)
        calendar = http.request.env['calendar.event'].search(
            [
                ('building_id', '=', building_id),
                ('is_ag', '=', True),
                ('start', '>=', start),
                ('stop', '<=', end),
            ], limit=1
        )

        return '%s %s' % (calendar.start.day, _Mois_fr.get(calendar.start.month)) if calendar else False

    @http.route('/timeline/statistics', type='json', auth='user')
    def get_timeline(self):
        today = date.today()

        dates = []

        dates.append((today-relativedelta(months=2)))
        dates.append((today-relativedelta(months=1)))
        dates.append((today+relativedelta(months=0)))
        dates.append((today+relativedelta(months=1)))
        dates.append((today+relativedelta(months=2)))
        dates.append((today+relativedelta(months=3)))

        buildings = http.request.env['syndic.building'].search(
            [
                ('ag_month', '!=', False),
                ('ag_month', 'in', [month.month for month in dates]),
            ],
        )

        events = []
        for month in dates:
            premiers = buildings.filtered(
                lambda s: s.ag_month == str(month.month) and s.ag_fortnight == '1'
            )

            first = []
            first_data = {}
            for premier in premiers:
                first_data = premier.read(['id', 'name', 'manager_id'])[0]
                first_data['is_set'] = self._get_is_set(month.year , month, 1, first_data['id'])
                first.append(first_data)

            deuxiemes = buildings.filtered(
                lambda s: s.ag_month == str(month.month) and s.ag_fortnight == '2'
            )

            last = []
            last_data = {}
            for deuxieme in deuxiemes:
                last_data = deuxieme.read(['id', 'name', 'manager_id'])[0]
                last_data['is_set'] = self._get_is_set(month.year, month, 2, last_data['id'])
                last.append(last_data)

            events.append({
                'month': month.month,
                'date': '%s - %s' % (month.year, _Mois_fr.get(month.month)),
                'premier': first,
                'deuxieme': last,
            })
        return {
            'myEvents': events
        }

    @http.route('/dashboard/buildings', type='json', auth='user')
    def get_buildings(self):
        uid = http.request.env['syndic.building']._context.get('uid')
        buildings = http.request.env['syndic.building'].search_read(
                [('manager_id', '=', uid)],
                ['name']
        )
        return {
            'buildings': buildings,
        }
