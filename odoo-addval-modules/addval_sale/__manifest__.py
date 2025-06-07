# -*- coding: utf-8 -*-
{
    "name": "Sale Configurations (Addval)",
    "summary": "Default configurations and improvements for Sale module (Addval)",
    "description": """This module has the following improvements:
    - Adds a new field to sale orders to store the customer reference date.
    - Adds Sale Order Report with Chilean legal requirements.""",
    "author": "Addval Connect",
    "website": "http://www.addval.cl",
    "category": "Accounting",
    "license": "Other proprietary",
    "version": "0.2",
    "depends": ["sale", "addval_accounting"],
    "data": [
        # "views/sale_order.xml",
        # "views/sale_report_templates.xml"
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
