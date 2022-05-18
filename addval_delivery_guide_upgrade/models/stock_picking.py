from odoo import models


class Picking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking"]

    # def _get_dte_template(self):
    #     return self.env.ref("addval_delivery_guide_upgrade.dte_template")
