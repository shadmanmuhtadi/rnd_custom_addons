
{
    'name': 'IDC Supply Chain Management',
    'author': 'IDCIT',
    'category': 'ERP',
    'sequence': 6,
    'summary': 'Manages the Supply Chain Process',
    'depends': ['stock','sale','purchase','mail','base','delivery','shipment_management_bs'],
    'images': [],
    'website': "",
    'description': """,
            """,
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/menu.xml',
        'views/hscode_view.xml',
        'views/lc_view.xml',
        'views/product_view.xml',
        'views/purchase_view.xml', 
        'views/master_view.xml',
        'views/shipment_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

