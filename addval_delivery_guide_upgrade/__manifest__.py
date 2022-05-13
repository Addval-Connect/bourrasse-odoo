# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Upgraded Delivery Guide (Addval)",
    "summary": "Upgraded Delivery Guide (Addval)",
    "category": "Customization",
    "description": "This upgrade the current format of generated delivery guides, as well as the generated xml sent to SII.",
    "depends": ["l10n_cl_edi_stock"],
    "version": "1.0",
    "auto_install": False,
    "license": "LGPL-3",
    "author": "Addval Connect",
    "website": "http://www.addval.cl",
    "data": [
        "views/report_delivery_guide.xml",
    ],
    "installable": True,
    "application": True,
}
