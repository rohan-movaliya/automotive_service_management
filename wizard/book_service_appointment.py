from odoo import fields, models


class BookAppointment(models.TransientModel):
    _name = "book.appointment"
    _description = "Book Appointment"

    # field for book appointment wizard 
    name = fields.Char(string="Customer Name", required=True)
    mobile_number = fields.Integer(required=True)
    customer_mail = fields.Char(required=True)
    car_model = fields.Char(string="Car Model Name", required=True)
    car_number = fields.Char(required=True)
    appointment_date = fields.Date(required=True)
    select_service = fields.Many2many(
        comodel_name="automotive.accessories", required=True
    )
    pick_up_address = fields.Char()
    drop_address = fields.Char()

    # method for book service appointment 
    def action_book_appointment(self):
        """this methos will create new record for service appointment """
        mechanics_vacance = self.env["automotive.mechanic"].search([])
        for mechanic in mechanics_vacance:
            if not mechanic.work_assigned:
                vals = {
                    "name": self.name,
                    "car_model": self.car_model,
                    "car_number": self.car_number,
                    "appointment_date": self.appointment_date,
                    "car_sevices_ids": self.select_service,
                    "contact_number": self.mobile_number,
                    "assigned_mechanic_id": mechanic.id,
                    "pick_up_address": self.pick_up_address,
                    "drop_address": self.drop_address,
                    "customer_mail": self.customer_mail,
                }
                self.env["service.appointment"].create(vals)
                break
