# -*- coding: utf-8 -*-

{
    'name': "Reportes Excel",
    'version': '18.0.1.0.0',
    'author': 'Vicente Opaso Valenzuela',
    'category': 'Technical Settings',
    "license": 'Other proprietary',
    'depends': [
        'base',
        'web'
    ],
    "external_dependencies": {"python": ["openpyxl"]},
    'data': [
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'excel_report/static/src/js/*',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
