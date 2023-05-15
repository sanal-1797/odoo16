# -*- coding: utf-8 -*-
from odoo import models, fields, api


class HotelRooms(models.Model):
    """for creating room"""

    _name = "hotel.rooms"
    _description = "Hotel Rooms"
    _inherit = 'mail.thread'
    _rec_name = "room_no"

    room_no = fields.Char(string="Room NO.", default='New', required=True, readonly=True, copy=False)
    bed = fields.Selection(string="Bed",
                           selection=[('single', 'Single'), ('double', 'Double'), ('dormitory', 'Dormitory')])

    available_beds = fields.Integer(string=" Available beds")
    facilities_ids = fields.Many2many('room.facilities', string="Facilities")
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    rent = fields.Monetary(string="rent")

    room_guest_id = fields.Many2one('res.partner')

    state = fields.Selection(
        selection=[
            ('available', "Available"),
            ('booked', "Booked"),

        ],
        string="Status",
        readonly=True, copy=False,
        default='available')

    acc_id = fields.Many2one('accommodation.guest')

    @api.model
    def create(self, vals):
        """for creating accommodation sequence"""
        if vals.get('room_no', 'New') == 'New':
            vals['room_no'] = self.env['ir.sequence'].next_by_code(
                'room.sequence') or 'New'
        return super().create(vals)
