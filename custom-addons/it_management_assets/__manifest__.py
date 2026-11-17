{
    'name': 'IT Device Management',
    'version': '18.0.1.1',
    'summary': 'Manajemen inventaris perangkat IT (Laptop, Printer, Server)',
    'category': 'IT',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/device_views.xml',
    ],
    'installable': True,
    'application': True,
}