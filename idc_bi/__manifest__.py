{
    'name': 'IDC BI Management',
    'version':'1.0.0',
    'category': 'BI',
    'author': 'Hemal Majumder & Shadman Muhtadi',
    'summary': 'BI Management System',
    'description':"""BI Management System for IDC""",
    'depends':[], #dependencies on other module
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/bi_view.xml',
    ], #here we will import all the xml file of this module
    'demo':[],
    'sequence': -99, #prioritized in the app list, lower the sequence higher the priority
    'application': True, #listed in app list when it is True, if set False then listed in module
    'installable': True, #installable when true
    'auto_install': False,
    'license': 'LGPL-3', #licence if you have one
}