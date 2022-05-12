# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Addval Update Invoice References',
    'summary': 'Updates references for invoices',
    'author': 'Addval Connect',
    'category': 'Customization',
    'description': "This module will update the invoice references.",
    'depends': ['account', 'l10n_cl', 'l10n_cl_edi'],
    'version': '1.0',
    'auto_install': False,
    'license': 'LGPL-3',
    'website': "http://www.odoo.com",
    'data': [
        'data/l10n_latam.document.type.csv',
    ],
    'installable': True,
    'application': True,
}
