from odoo import fields, models
from odoo.exceptions import ValidationError


class CancelAppointment(models.TransientModel):
    _name = "cancel.appointment"
    _description = "Cancel Appointment"

    appointment_ids = fields.Many2one(
        string="Select Appointment", comodel_name="service.appointment"
    )

    # method for cancel appointment 
    def action_cancel_service_appointment(self):
        """method for cancel service appointment if state is appointed otherwise
        raise validation error """
        if self.appointment_ids.state == "appointed":
            self.appointment_ids.unlink()
        else:
            raise ValidationError(
                f"In {self.appointment_ids.state} State You can Not Cancel Appointment"
            )
