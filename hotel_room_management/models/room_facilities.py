# -*- coding: utf-8 -*-
from odoo import models, fields


class RoomFacilities(models.Model):
    """Room facilities"""
    _name = "room.facilities"
    _rec_name = "facility_name"

    facility_name = fields.Char(string="Facilities")
    color = fields.Integer(string="Color")
