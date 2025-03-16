from odoo.tests.common import TransactionCase


class TestAutomotiveAccessories(TransactionCase):
    def setUp(self):
        super(TestAutomotiveAccessories, self).setUp()
        self.accessories_01 = self.env["automotive.accessories"].create(
            {
                "name": "car accessories",
                "service_charge": 100,
                "accessories_name": "car accessories",
            }
        )

    def test_01_some_actions(self):
        self.assertEqual(self.accessories_01.name, "car accessories")
        self.assertEqual(self.accessories_01.service_charge, 100)
