# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class FacturationSyndic(models.Model):
    _name = 'syndic.facturation.syndic'
    _inherit = 'syndic.facturation'
    _report_name = 'sgimmo_facturation.facture'
    _order = 'id desc'
