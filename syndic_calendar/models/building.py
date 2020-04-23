# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions

from dateutil.relativedelta import relativedelta


class Building(models.Model):
    _inherit = 'syndic.building'

    calendar_ids = fields.One2many('calendar.event', 'building_id', 'Calendriers')
    is_ag_ready = fields.Boolean('AG Organisé', compute='_get_ag_ready')
    last_ag_date = fields.Date('Derniere AG', compute='_get_ag_ready')

    def _get_ag_ready(self):
        today = fields.datetime.now()
        delay = self.env.company.month_delay
        beforemonth = today-relativedelta(months=delay)
        aftermonth = today+relativedelta(months=delay)

        for building in self:
            calendar = building.calendar_ids.filtered(lambda s: s.is_ag and str(s.start.month) == building.date_mois and s.start.year == today.year)

            if calendar and calendar[0].start > beforemonth and calendar[0].start < aftermonth:
                building.is_ag_ready = True
                building.last_ag_date = calendar[0].start
            else:
                building.is_ag_ready = False
                building.last_ag_date = False
