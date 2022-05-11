# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Vendor bills report (Addval)',
    'summary': 'Custom Vendor bills report (Addval)',
    'author': 'Odoo PS',
    'category': 'Customization',
    'description': "This module will change the vendor bill report layout.",
    'depends': ['account', 'l10n_cl', 'l10n_cl_edi'],
    'version': '1.0',
    'auto_install': False,
    'license': 'LGPL-3',
    'website': "http://www.odoo.com",
    'data': [
        'views/report_invoice.xml',
        'data/l10n_latam.document.type.csv',
    ],
    'installable': True,
    'application': True,
}
