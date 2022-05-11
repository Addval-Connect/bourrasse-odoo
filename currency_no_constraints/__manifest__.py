# -*- coding: utf-8 -*-
{
    "name": "addval_currency_no_constraints",
    "summary": "Use this with caution.",
    "description": "This module disables the currency constraints.",
    "author": "Addval Connect",
    "website": "http://www.addval.cl",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    "category": "Accounting/Localizations/Account Charts",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": [
        "account",
    ],
    # always loaded
    "data": [
        # 'security/ir.model.access.csv',
        # "views/views.xml",
        # "views/templates.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        # "demo/demo.xml",
    ],
}
