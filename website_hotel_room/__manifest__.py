# -*- coding: utf-8 -*-

{
    'name': "Hotel Room Booking Website",
    'version': '16.0.1.0.0',
    'depends': ['base', 'website'],
    'data': [
        'views/hotel_room_website_menu.xml',
        'views/online_hotel_room_booking_form.xml'
    ],
    'assets': {
        'web.assets_frontend': ['/website_hotel_room/static/src/js/online_hotel_room_booking.js']},
    'description': """
    Hotel Room Booking Website 
    """,
    'installable': True,
    'author': "Sanal"
}
