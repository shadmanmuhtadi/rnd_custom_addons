{
    'name': 'IDC Inventory Management',
    'version':'1.0.0',
    'category': 'IDC Inventory',
    'author': 'Hemal Majumder',
    'summary': 'Inventory Management System',
    'description':"""Inventory Management System for IDC""",
    'depends':['product', 'hr'], #dependencies on other module
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/product_template_view.xml',
        'views/product_category_view.xml',
        'views/product_it_requisition_view.xml',
        'views/product_vendor_name_view.xml',
        'views/menu.xml'
    ], #here we will import all the xml file of this module
    'demo':[],
    'sequence': -98, #prioritized in the app list, lower the sequence higher the priority
    'application': True, #listed in app list when it is True, if set False then listed in module
    'installable': True, #installable when true
    'auto_install': False,
    'license': 'LGPL-3', #licence if you have one
}