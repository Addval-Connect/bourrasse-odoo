# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):

    _name = "sale.order"
    _inherit = ["sale.order"]

    client_order_ref = fields.Char(string="Customer Reference", copy=False)
    client_order_date = fields.Date(string="Customer Reference Date", copy=False)
