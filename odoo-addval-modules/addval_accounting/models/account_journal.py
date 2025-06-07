# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    read_dte = fields.Boolean(
        default=False,
        string="Give DTE priority",
        help="Set active to give priority when reading DTEs",
    )
