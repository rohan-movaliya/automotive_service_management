from odoo.tests.common import TransactionCase


class TestWizardServicePayment(TransactionCase):
    # setUP method for create record for test cases 
    def setUp(self):
        super(TestWizardServicePayment, self).setUp()
        # create record for appointment_01 
        self.appointment_01 = self.env["service.appointment"].create(
            {
                "name": "Ranveer",
                "contact_number": 1234567891,
                "customer_mail": "ranveer@bizzappdev.com",
                "car_model": "BMW",
                "car_number": "GJ08GY4785",
                "appointment_date": "2024-12-12",
                "car_sevices_ids": self.env.ref(
                    "automotive_service_management.automotive_accessories_1"
                ),
                "assigned_mechanic_id": self.env.ref(
                    "automotive_service_management.automotive_mechanic_6"
                ).id,
            }
        )

        self.appointment_01.button_in_service()

        self.appointment_01.button_serviced()

        self.service_payment_01 = self.env["service.payment"].create(
            {
                "appointment_id": self.appointment_01.id,
                "payment_reference_number": "AP000123",
            }
        )

    # method for call payment wizard 
    def test_service_payment(self):
        """this method is called when appointment is in serviced state"""
        self.service_payment_01.get_amount()
        self.service_payment_01.action_payment_done()
