{
    'name': "Import Order Lines",
    'version': '16.0.1.0.0',
    'depends': ['base','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'wizard/import_order_line_wizard_views.xml'
    ],
    'description': """
    Import Order Lines
    """,
    'installable': True,
    'author': "Sanal",
    'sequence': 4

}
