# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"
    _sql_constraints = [
        (
            "check_credit_debit",
            "CHECK(1=1)",
            "Wrong credit or debit value in accounting entry !",
        ),
        (
            "check_accountable_required_fields",
            "CHECK(1=1)",
            "Missing required account on accountable invoice line.",
        ),
        (
            "check_non_accountable_fields_null",
            "CHECK(1=1)",
            "Forbidden unit price, account and quantity on non-accountable invoice line",
        ),
        (
            "check_amount_currency_balance_sign",
            "CHECK(1=1)",
            "The amount expressed in the secondary currency must be positive when account is debited and negative when "
            "account is credited. If the currency is the same as the one from the company, this amount must strictly "
            "be equal to the balance.",
        ),
    ]
