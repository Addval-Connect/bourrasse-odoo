# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"
    _sql_constraints = []
