from odoo import models,  fields
from datetime import datetime


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="postcode")
    date_availability = fields.Date(string="Date availability",copy=False,default=datetime.today())
    expected_price = fields.Float(string="Expected price")
    selling_price = fields.Float(string="selling price",readonly=True,copy=False)
    bedrooms = fields.Integer(string="Bedroom",default=2)
    living_area = fields.Integer(string="Living area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="garage")
    garden = fields.Boolean(string="Boolean")
    garden_area = fields.Integer(string="Garden area")
    garden_orientation = fields.Selection(string="Garden orientation",selection=[('north', 'North'), ('south', 'South'),('east', 'East'),('west', 'West')])



