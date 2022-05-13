from odoo import models


class Picking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking"]

    def print_delivery_guide_pdf(self):
        return self.env.ref(
            "addval_delivery_guide_upgrade.action_delivery_guide_report_pdf"
        ).report_action(self)
