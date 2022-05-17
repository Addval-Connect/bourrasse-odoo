from odoo import models


class Picking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking"]
