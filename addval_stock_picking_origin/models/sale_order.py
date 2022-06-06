# -*- coding: utf-8 -*-

from odoo import _, fields, models


class Picking(models.Model):
    """Extension of base stock picking model to add origin document to stock pickings"""

    _name = "stock.picking"
    _inherit = ["stock.picking"]

    origin_sale = fields.Many2one("sale.order", string="Origin Document", readonly=True)
