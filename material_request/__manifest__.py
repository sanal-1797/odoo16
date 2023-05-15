{
    'name': "Material Request",
    'version': '16.0.1.0.0',
    'depends': ['base', 'mail', 'product', 'purchase'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/material_request_sequence.xml',
        'views/material_request_views.xml',
        'views/material_request_menus.xml',
        'views/product_lines_views.xml',
    ],
    'category': 'material/request',
    'description': """
    Material Request
    """,
    'application': True,
    'installable': True,
    'author': "Sanal",
    'sequence': 2

}
