{
    'name': 'Occupational Health Tracking',
    'version': '17.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Track mandatory employee medical checks',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'data/ir_cron.xml',
    ],
    'installable': True,
    'application': False,
}