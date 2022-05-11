# -*- coding: utf-8 -*-
{
    "name": "journal_entry_edditor_addval",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "Addval Connect",
    "website": "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    "category": "Accounting/Localizations/Account Charts",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": [
        "contacts",
        "base_address_city",
        "base_vat",
        "l10n_latam_base",
        "l10n_latam_invoice_document",
        "uom",
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
