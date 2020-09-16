# -*- coding: utf-8 -*-
from odoo.tests import common
from odoo.exceptions import AccessError

from datetime import datetime

class TestSyndicCommon(common.TransactionCase):

    def setUp(self):
        super(TestSyndicCommon, self).setUp()

        # Usefull models
        self.Users = self.env['res.users']
        self.Building = self.env['syndic.building']
        self.Lot = self.env['syndic.lot']

        # User groups
        self.serge = self.env['ir.model.data'].xmlid_to_res_id('syndic_base.syndic_user_serge')
        self.sandrine = self.env['ir.model.data'].xmlid_to_res_id('syndic_base.syndic_user_sandrine')
        self.florence = self.env['ir.model.data'].xmlid_to_res_id('syndic_base.syndic_user_florence')

        # city
        self.wavre = self.env['ir.model.data'].xmlid_to_res_id('syndic_base.2701')

        # building
        self.gemini = self.env['ir.model.data'].xmlid_to_res_id('syndic_base.syndic_demo_building_gemini')

        # owner
        self.sgimmo = self.env['ir.model.data'].xmlid_to_res_id('syndic_base.syndic_partner_gemini_owner')

        # Lot
        self.A1 = self.env['ir.model.data'].xmlid_to_res_id('syndic_base.syndic_gemini_lot1')
        self.A2 = self.env['ir.model.data'].xmlid_to_res_id('syndic_base.syndic_gemini_lot2')

        self.owner1 = self.env['ir.model.data'].xmlid_to_res_id('syndic_base.syndic_partner_gemini_owner')
        self.owner2 = self.env['ir.model.data'].xmlid_to_res_id('syndic_base.syndic_partner_syndic_owner')


class TestBuildingFlow(TestSyndicCommon):

    def test_00_building_creation(self):
        vals = {
            'name': 'ADFL',
            'num_building': '46',
            'zip': 1300,
            'city_id': self.wavre,
            'street': 'Rue Edouard Olivier, 27',
        }
        with self.assertRaises(AccessError):
            self.Building.with_user(self.serge).create(vals)

        self.adfl = self.Building.with_user(self.sandrine).create(vals)
        self.aloys = self.Building.with_user(self.florence).create({
            'name': 'ALOYS',
            'num_building': '140',
            'zip': 1300,
            'city_id': self.wavre,
            'street': 'Boulevard du Souverain 338',
            'bank_ids': [(
                0,
                0,
                {
                    'acc_number': 'BE11 0689 3168 7148',
                }
            )],
        })
        
        self.aloys.read([
            'total_quotites',
            'lot_count',
            'owner_count',
            'loaner_count',
            'contract_count',
        ])

        self.aloys.action_inhabitant()
        self.aloys.with_context(inhabitant_type='owner').action_inhabitant()
        self.aloys.with_context(inhabitant_type='loaner').action_inhabitant()
        self.aloys.action_contract()
        self.aloys._onchange_zip()
        self.aloys.action_lot()
        self.aloys.open_sign()
        self.aloys.fiche_signalitic_ids._onchange_check_exist()
        self.aloys.toggle_lock()

        self.aloys.toggle_active()
        self.assertEqual(self.aloys.active, False)
        self.aloys.toggle_active()
        self.assertEqual(self.aloys.active, True)
        self.aloys.unlink()

    def test_01_partner(self):
        owner = self.env['res.partner'].browse(self.owner1)
        self.env['res.partner'].with_context(normal_create=True).create({
            'name': 'Test Partner',
        })
        owner.action_lot()
        owner.action_lot_loaner()
        owner.action_lot_old()
        owner._onchange_zip()

        owner.read([
            'old_lot_count',
            'loaner_lot_count',
            'lot_count',
            'owner_building_ids',
        ])

        owner.search([
            ('owner_building_ids', '=', self.gemini)
        ])

    def test_02_mutation(self):
        lot = self.env['syndic.lot'].browse(self.A2)
        new_mutation = self.env['syndic.mutation'].create({
            'mutation_date': datetime.now(),
            'old_partner_ids': [(6, 0, [lot.owner_id.id])],
            'new_owner_id': self.env['res.partner'].create({'name': 'NEW mutation'}).id,
            'lot_ids': [(6, 0, [lot.id])],
        })

        old_partner = self.env['res.partner'].browse(self.owner2)
        self.assertEqual(old_partner.is_old, False)
        new_mutation.mutation()
        self.assertEqual(old_partner.is_old, True)
        new_mutation.read(['name'])
        new_mutation.onchange_old_owner()
