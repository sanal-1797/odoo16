# -*- coding: utf-8 -*-
from odoo import models, fields


class GuestDetails(models.Model):
    """Guest details"""
    _name = "guest.details"

    partner_id = fields.Many2one('res.partner', string='Guest', required=True)
    gender = fields.Selection(string='Gender',
                              selection=[('male', 'Male'), ('female', 'Female')], required=True)
    age = fields.Integer(string='Age', required=True)

    reference_id = fields.Many2one('accommodation.guest')
