# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Stock Picking Origin Document (Addval)",
    "summary": "This module changes the origin field of stock pickings to directly link to the document that created de pciking, if it exists.",
    "category": "Customization",
    "description": "",
    "depends": ["stock,sale"],
    "version": "1.0",
    "auto_install": False,
    "license": "LGPL-3",
    "author": "Addval Connect",
    "website": "http://www.addval.cl",
    "data": [
        # "views/report_invoice.xml",
    ],
    "installable": True,
    "application": True,
}
