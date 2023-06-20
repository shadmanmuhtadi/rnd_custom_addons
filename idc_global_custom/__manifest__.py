

{
    'name': 'Global Customization',
    'version': '1.0',
    'category': 'Hidden',
    'author': 'Imran Ahmed',
    'summary': 'Global customization',
    'description':"""Global Customization""",
    'depends': ['web'],
    'data': [
        "views/login_page_custom.xml"
    ],
    'assets': {
        'web.assets_backend': [
            'idc_global_custom/static/src/js/app_window_title.js',
        ],
    },
    'demo': [
    ],
    'sequence': -100,
    'application': True,
    'installable': True,
    'auto_install': False,
}
