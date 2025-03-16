from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestServiceAppointment(TransactionCase):
    # setUP method for create record for test cases 
    def setUp(self):
        super(TestServiceAppointment, self).setUp()
        # create record for appointment_01 
        self.mechanic_01 = self.env["automotive.mechanic"].create({"name": "Prince"})
        self.accessories_01 = self.env["automotive.accessories"].create(
            {
                "name": "accessories",
                "service_charge": 100,
                "accessories_name": "accessories",
            }
        )

        self.appointment_01 = self.env["service.appointment"].create(
            {
                "name": "Rohan",
                "contact_number": 123456789,
                "customer_mail": "rohan@bizzappdev.com",
                "car_model": "VOLVO",
                "car_number": "GJ02DR5677",
                "car_sevices_ids": self.accessories_01,
                "assigned_mechanic_id": self.mechanic_01.id,
            }
        )
        self.appointment_01.button_appointed()
        self.appointment_01.action_send_mail()
        self.appointment_01._compute_delivery_date()
        self.appointment_01._compute_total_cost()
        self.appointment_01.name_search(self, args=None, operator="ilike", limit=100)

        # create record for mechanic 
        self.mechanic_02 = self.env["automotive.mechanic"].create({"name": "Peter"})
        # create record for appointment_02 
        self.appointment_02 = self.env["service.appointment"].create(
            {
                "name": "Mohan",
                "car_model": "Audi",
                "contact_number": 123456789,
                "customer_mail": "mohan@bizzappdev.com",
                "car_number": "GJ02DR5677",
                "assigned_mechanic_id": self.mechanic_02.id,
            }
        )
        # create record for appointment_03 
        self.appointment_03 = self.env["service.appointment"].create(
            {
                "name": "Ketan",
                "contact_number": 123456789,
                "customer_mail": "ketan@bizzappdev.com",
                "car_model": "BMW",
                "car_number": "GJ02DR5677",
                "assigned_mechanic_id": self.mechanic_02.id,
            }
        )
        self.appointment_02.button_in_service()

        # assertRaises for handle ValidationError 
        with self.assertRaises(ValidationError):
            self.appointment_03.button_in_service()

    # method for check the output of function 
    def test_service_appointment(self):
        self.assertEqual(self.appointment_01.total_cost, 100)
        self.assertEqual(self.appointment_01.state, "appointed")

        self.appointment_01.button_in_service()
        self.appointment_01.button_serviced()
        self.assertEqual(self.appointment_01.state, "serviced")
        self.assertEqual(self.appointment_01.assigned_mechanic_id.work_assigned, False)

        self.appointment_02.button_appointed()
        self.assertEqual(self.appointment_02.state, "appointed")

        records = self.env["service.appointment"].name_search(
            name="Ketan", operator="ilike"
        )
        self.assertIn(self.appointment_03.id, [record[0] for record in records])
