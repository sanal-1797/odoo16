{
    'name': "Top 10 Customers",
    'version': '16.0.1.0.0',
    'depends': ['base'],
    'data': [
        'views/top_10_customers.xml',
        'views/customer_details.xml'
    ],
    'assets': {
        'web.assets_frontend': ['/top_10_customers/static/src/js/top_10_customers.js']},
    'description': """
    Top 10 Customers 
    """,
    'installable': True,
    'author': "Sanal"
}
