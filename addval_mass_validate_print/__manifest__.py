# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Bulk Customer invoices validate and print (Addval)',
    'summary': 'Bulk Customer invoices validate and print (Addval)',
    'author': 'Odoo PS',
    'category': 'Customization',
    'description': "This module helps to validate bulk Customer invoices and bulk print.",
    'depends': ['account'],
    'version': '1.0',
    'license': 'LGPL-3',
    'website': "http://www.odoo.com",
    'data': [
        'data/account_journal.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
