{
    'name': "Approval Block",
    'version': '16.0.1.0.0',
    'depends': ['base', 'mail','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'data/approval_block_data.xml',
        'views/approval_block_views.xml',
        'views/approval_block_menus.xml',
        'views/purchase_order_views.xml',
    ],
    'description': """
    Approval Block
    """,
    'application': True,
    'installable': True,
    'author': "Sanal",
    'sequence': 3

}
