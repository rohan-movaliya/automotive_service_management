from odoo import fields, models


class AutomotiveMechanic(models.Model):
    _name = "automotive.mechanic"
    _description = "Automotive Mechanic"
    _inherit = ["image.mixin"]

    # fields for automotive mechanic
    name = fields.Char(string="Mechanic Name")
    work_assigned = fields.Boolean()
    repaired_cars_ids = fields.Many2many(
        string="Repaired Cars", comodel_name="service.appointment"
    )
    image_256 = fields.Image(
        string="Profile Image", readonly=False, max_width=256, max_height=256
    )
