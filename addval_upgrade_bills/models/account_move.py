# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_name_invoice_report(self):
        self.ensure_one()
        if self.move_type == 'in_invoice':
            return 'addval_upgrade_bills.report_invoice_document'
        return super()._get_name_invoice_report()

