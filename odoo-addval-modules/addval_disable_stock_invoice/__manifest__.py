# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Disable Stock Invoice (Addval)",
    "summary": "Disable Stock Invoice (Addval)",
    "category": "Customization",
    "description": "This module will forcefully disable stock/lot information to appear on invoice reports.",
    "depends": ["stock_account"],
    "version": "1.0",
    "auto_install": False,
    "license": "Other proprietary",
    "author": "Addval Connect",
    "website": "http://www.addval.cl",
    "data": [
        # "views/report_invoice.xml",
    ],
    "installable": True,
    "application": True,
}
