# -*- coding: utf-8 -*-
{
    "name": "Accounting Configurations (Addval)",
    "summary": "Default configurations and improvements for Accounting module (Addval)",
    "description": """This module has the following improvements:
    - Generated vendor bills now follow Chilean laws.
    - Transferable documents are now supported.
    - Bulk Customer invoices validation and printing.
    - Adds account reference document 820 to customer invoices options.
    - Adds a monetary widget that always shows two decimals, regardless of the currency.
    - Adds default journal selecction to customer invoices.""",
    "author": "Addval Connect",
    "website": "http://www.addval.cl",
    "category": "Accounting",
    "license": "Other proprietary",
    "version": "0.2",
    "depends": ["account", "l10n_cl", "l10n_cl_edi", "base"],
    "data": [
        # "views/account_move_views.xml",
        # "views/account_journal_views.xml",
        # "views/report_templates.xml",
        # "views/report_invoice.xml",
        # "data/l10n_latam.document.type.csv",
        # "data/account_journal.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
