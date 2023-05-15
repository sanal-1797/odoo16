{
    'name': "Employee Transfer",
    'version': '16.0.1.0.0',
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_transfer_views.xml',
        'views/employee_transfer_menus.xml',
    ],
    'description': """
    Employee Transfer
    """,
    'application': True,
    'installable': True,
    'author': "Sanal",
    'sequence': 1

}
