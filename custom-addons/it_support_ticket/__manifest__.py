{
    'name': 'IT Support Ticket',
    'version': '1.0',
    'summary': 'Modul sederhana untuk manajemen tiket dukungan IT',
    'category': 'Helpdesk',
    'depends': ['base', 'mail'],  # <-- PASTIKAN 'mail' ADA DI SINI
    'data': [
        'security/it_support_security.xml',
        'security/it_support_rules.xml',
        'security/ir.model.access.csv',
        'views/ticket_views.xml',
    ],
    'installable': True,
    'application': True,
}