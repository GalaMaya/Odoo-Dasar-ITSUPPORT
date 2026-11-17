{
    'name': 'IT Support Ticket',
    'version': '1.1',
    'summary': 'Modul sederhana untuk manajemen tiket dukungan IT',
    'category': 'Helpdesk',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'it_management_assets'],
    'data': [
        'security/it_support_security.xml',
        'security/it_support_rules.xml',
        'security/ir.model.access.csv',
        'reports/ticket_report.xml',
        'views/ticket_views.xml',
        'views/device_views.xml',
    ],
    'installable': True,
    'application': True,
}