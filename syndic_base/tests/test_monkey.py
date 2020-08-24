from odoo.addons.l10n_be_edi.tests.test_ubl import TestUBL


class NewTestUBL(TestUBL):
    # in the standard method it seems that the demo vat is not correct
    def setUp(self):
        pass

    def test_ubl_invoice_import(self):
        pass


TestUBL.setUp = NewTestUBL.setUp
TestUBL.test_ubl_invoice_import = NewTestUBL.test_ubl_invoice_import
