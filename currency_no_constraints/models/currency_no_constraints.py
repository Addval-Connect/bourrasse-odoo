# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models

class ResCurrency(models.Model):
    _inherit = 'res.currency'

    def _has_accounting_entries(self):
        return False
