# -*- coding: utf-8 -*-
{
    'name': 'Purchase Order to Proforma Invoice',
    'summary': "Create Proforma invoice of purchase order",
    'author': "IDCIT",
    'sequence': -999,
    'website': "",

    'license': 'OPL-1',
    'category': 'Purchase',
    'version': '15.0.0.1',

    'depends': ['base','purchase','stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/po_view.xml',
        'views/pi_view.xml',
        'views/lc_view.xml',
    ],
    'application': True,
    'installable': True,
    'currency': 'USD'
}


