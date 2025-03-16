from datetime import date

from dateutil import relativedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ServiceAppointment(models.Model):
    _name = "service.appointment"
    _description = "Service Appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # fields for automotive service appointment
    name = fields.Char(string="Customer Name", required=True)
    contact_number = fields.Char(string="Mobile Number", required=True)
    customer_mail = fields.Char(required=True)
    appointment_number = fields.Char(readonly=True)
    car_model = fields.Char(required=True)
    car_number = fields.Char(required=True)
    appointment_date = fields.Date(default=date.today())
    delivery_date = fields.Date(
        string="Estimate Delivery Date", compute="_compute_delivery_date"
    )
    car_sevices_ids = fields.Many2many(
        comodel_name="automotive.accessories", string="Services"
    )
    assigned_mechanic_id = fields.Many2one(
        comodel_name="automotive.mechanic", string="Assigned To"
    )
    total_cost = fields.Integer(compute="_compute_total_cost", readonly="True")
    payment_reference_number = fields.Char()
    pick_up_address = fields.Char()
    drop_address = fields.Char()

    state = fields.Selection(
        [
            ("appointed", "Appointed"),
            ("in_service", "In Service"),
            ("serviced", "Serviced"),
            ("payment_done", "Payment Done"),
        ],
        string="Status",
        required=True,
        default="appointed",
        tracking=True,
    )

    customer_feedback = fields.Selection(
        [
            ("0", "Very Low"),
            ("1", "Low"),
            ("2", "Normal"),
            ("3", "High"),
            ("4", "Very High"),
            ("5", "Excellent"),
        ],
        default="0",
    )

    # button for change state
    def button_appointed(self):
        """button for change state into appointed """
        self.write({"state": "appointed"})

    # button for change state 
    def button_in_service(self):
        """button for validation if mechanic is busy than raise validation error
        otherwise it is assign work to the mechanic """
        for mechanic in self.assigned_mechanic_id:
            if mechanic.work_assigned:
                raise ValidationError(
                    f"{mechanic.name} is busy please select another one or wait."
                )
            else:
                mechanic.write({"work_assigned": "True"})
                self.write({"state": "in_service"})

    # button for change state 
    def button_serviced(self):
        """this function is for set state to serviced and add record to mechanic
        serviced car after that send mail to the customer for pick up the car """
        mechanics = self.env["automotive.mechanic"].search([])
        for record in mechanics:
            if record.name == self.assigned_mechanic_id.name:
                record.repaired_cars_ids = [(4, self.id)]
                record.write({"work_assigned": False})
                self.write({"state": "serviced"})

        mail_template = self.env.ref("automotive_service_management.serviced_car_mail")
        mail_template.send_mail(self.id, force_send=True)

    # create inherit method for sequence 
    @api.model
    def create(self, vals):
        vals["appointment_number"] = self.env["ir.sequence"].next_by_code(
            "service.appointment"
        )
        return super(ServiceAppointment, self).create(vals)

    # name_get method for concate the name and appointment number 
    @api.depends("name", "appointment_number")
    def name_get(self):
        record_list = []
        for record in self:
            record_list.append(
                (record.id, "[%s] : [%s]" % (record.appointment_number, record.name))
            )
        return record_list

    # name_search method for search many2one field 
    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []
        if name:
            recs = self.search(
                ["|", ("appointment_number", operator, name), ("name", operator, name)]
            )
            return recs.name_get()
        return self.search([("name", operator, name)] + args, limit=limit).name_get()

    # _compute_delivery_date for calculate estimate delivery date of car service 
    @api.depends("appointment_date")
    def _compute_delivery_date(self):
        """calculate delivery date from days given in system parameter"""
        service_duration = self.env["ir.config_parameter"].get_param(
            "automotive_service_management.service_duration"
        )
        for record in self:
            record.delivery_date = (
                record.appointment_date
                + relativedelta.relativedelta(days=int(service_duration))
            )

    # action_send_mail for send mail to customer after the service is completed 
    def action_send_mail(self):
        """this method is for send mail to customer after service is completed of car"""
        records = self.env["service.appointment"].search([])
        for record in records:
            if record.appointment_date == date.today():
                mail_template = self.env.ref(
                    "automotive_service_management.service_appointment_mail"
                )
                mail_template.send_mail(record.id, force_send=True)

    # _compute method for calculate total cost of the taken serviced
    @api.depends("car_sevices_ids")
    def _compute_total_cost(self):
        """this method is calculate total cost from product that is used from
        customer"""
        for record in self:
            sum_of_lines = sum(record.car_sevices_ids.mapped("service_charge"))
            record.total_cost = sum_of_lines
