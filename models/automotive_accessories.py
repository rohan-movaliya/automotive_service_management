from odoo import fields, models


class AutomotiveAccessories(models.Model):
    _name = "automotive.accessories"
    _description = "Automotive Accessories"
    _inherit = ["image.mixin"]

    # fields for automotive accessories 
    name = fields.Char(string="Service Name")
    service_charge = fields.Integer()
    accessories_name = fields.Char()
    image_256 = fields.Image(
        string="Accessories Image", readonly=False, max_width=256, max_height=256
    )
