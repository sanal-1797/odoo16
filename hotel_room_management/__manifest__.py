{
    'name': "Hotel Room Management",
    'version': '16.0.1.0.0',
    'depends': ['base', 'mail', 'account_payment', 'purchase', 'account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/hotel_room_views.xml',
        'views/accommodation_views.xml',
        'views/facilities_views.xml',
        'views/order_food_views.xml',
        'views/order_category_view.xml',
        'views/order_items_views.xml',
        'views/order_list_views.xml',
        'views/payment_guest_views.xml',
        'wizard/report_hotel_wizard.xml',
        'reports/hotel_report.xml',
        'reports/hotel_report_templates.xml',
        'data/guest_sequence.xml',
        'data/room_sequence.xml',
        'data/order_sequence.xml',
        'views/hotel_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hotel_room_management/static/src/js/action_manager.js'
        ]},
    'author': "Sanal",
    'application': True

}
