# -*- coding: utf-8 -*-
{
    "name": "Purchase Configurations (Addval)",
    "summary": "Default configurations and improvements for Purchase module (Addval)",
    "description": """This module has the following improvements:
    - Defaul purchase quotation template
    - Default purchase order template.""",
    "author": "Addval Connect",
    "website": "http://www.addval.cl",
    "category": "Accounting",
    "license": "Other proprietary",
    "version": "0.2",
    "depends": ["purchase", "addval_accounting"],
    "data": [
        # "views/purchase_order_templates.xml",
        # "views/purchase_quotation_templates.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
