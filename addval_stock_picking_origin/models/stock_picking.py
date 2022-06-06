# -*- coding: utf-8 -*-

from odoo import _, fields, models


class SaleOrder(models.Model):
    """Extension of base Sale  Order model to add origin document to stock pickings"""

    _name = "sale.order"
    _inherit = ["sale.order"]

    pickings = fields.One2many(
        "stock.picking", string="Origin Document","origin_sale", "Picking orders generated from this sale order"
    )
