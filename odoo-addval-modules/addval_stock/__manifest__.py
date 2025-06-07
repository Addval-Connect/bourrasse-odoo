# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Stock Configurations (Addval)",
    "summary": "Default configurations and improvements for Stock module (Addval)",
    "description": """This module has the following improvements:
       - Default delivery guide template.
       - Default delivery guide SII xml.""",
    "author": "Addval Connect",
    "website": "http://www.addval.cl",
    "category": "Stock",
    "license": "Other proprietary",
    "version": "0.2",
    "depends": ["stock", "addval_accounting", "l10n_cl_edi", "addval_sale"],
    "data": [
        # "views/report_delivery_guide.xml",
        # "views/stock_picking.xml",
        # "template/dte_template.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
