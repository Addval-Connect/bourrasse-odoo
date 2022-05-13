from odoo import models


class Picking(models.Model):
    _name = "stock.picking"
    _inherit = ["l10n_cl_edi_stock", "stock.picking"]
