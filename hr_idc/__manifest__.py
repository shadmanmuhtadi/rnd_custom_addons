

{
    'name': 'IDC HR',
    'version': '1.1',
    'category': 'Human Resources/Employees',
    'sequence': -99,
    'summary': 'Centralize employee information',
    'description': "",
    'website': '',
    'images': [
    ],
    'depends': [
        'base',
        'base_setup',
        'mail',
        'resource',
        'calendar',
        'web',
        'hr',
        'hr_attendance',
        'hr_contract',
        'hr_employee_updation',
        'oh_employee_documents_expiry',
        # 'hr_payroll_community',
        'hr_org_chart_overview',
        'idc_bi',
        'idc_offtake'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/meeting_room_data.xml',
        'views/menu.xml',
        'views/personal_info_view.xml',
        'views/idc_hr_contract.xml',
        'views/contact_inherit.xml',
        'views/designations.xml',
        'views/calendar_view.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
