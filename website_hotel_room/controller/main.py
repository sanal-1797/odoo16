# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class HotelWebsiteForm(http.Controller):
    @http.route(['/hotel'], type='http', auth="user", website=True)
    def room_booking(self):
        partners = request.env['res.partner'].sudo().search([])
        facilities = request.env['room.facilities'].sudo().search([])
        print(facilities)
        rooms = request.env['hotel.rooms'].sudo().search([])
        print(rooms)
        values = {}
        values.update({
            'partners': partners,
            'facilities': facilities
        })
        return request.render("website_hotel_room.online_hotel_room_booking_form", values)
