from odoo import models


class Picking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking"]

    def _l10n_cl_get_tax_amounts(self):
        """
        Calculates the totals of the tax amounts on the picking
        :return: totals, retentions, line_amounts
        """
        totals = {
            "vat_amount": 0,
            "subtotal_amount_taxable": 0,
            "subtotal_amount_exempt": 0,
            "vat_percent": False,
            "total_amount": 0,
        }
        retentions = {}
        line_amounts = {}
        guide_price = self.partner_id.l10n_cl_delivery_guide_price
        if guide_price == "none":
            return totals, retentions, line_amounts
        # No support for foreign currencies: fallback on product price
        if guide_price == "sale_order" and (
            not self.sale_id or self.sale_id.currency_id != self.company_id.currency_id
        ):
            guide_price = "product"
        max_vat_perc = 0.0
        move_retentions = self.env["account.tax"]
        for move in self.move_lines:
            if guide_price == "product" or not move.sale_line_id:
                taxes = move.product_id.taxes_id.filtered(
                    lambda t: t.company_id == self.company_id
                )
                price = move.product_id.lst_price
                qty = move.product_qty
            elif guide_price == "sale_order":
                sale_line = move.sale_line_id
                taxes = sale_line.tax_id
                qty = move.product_uom._compute_quantity(
                    move.product_uom_qty, sale_line.product_uom
                )
                price = sale_line.price_unit * (1 - (sale_line.discount or 0.0) / 100.0)

            tax_res = taxes.compute_all(
                price,
                currency=self.company_id.currency_id,
                quantity=qty,
                partner=self.partner_id,
            )
            totals["total_amount"] += tax_res["total_included"]

            no_vat_taxes = True
            for tax_val in tax_res["taxes"]:
                tax = self.env["account.tax"].browse(tax_val["id"])
                if tax.l10n_cl_sii_code == TAX19_SII_CODE:
                    no_vat_taxes = False
                    totals["vat_amount"] += tax_val["amount"]
                    max_vat_perc = max(max_vat_perc, tax.amount)
                elif tax.tax_group_id.id in [
                    self.env.ref("l10n_cl.tax_group_ila").id,
                    self.env.ref("l10n_cl.tax_group_retenciones").id,
                ]:
                    retentions.setdefault((tax.l10n_cl_sii_code, tax.amount), 0.0)
                    retentions[(tax.l10n_cl_sii_code, tax.amount)] += tax_val["amount"]
                    move_retentions |= tax
            if no_vat_taxes:
                totals["subtotal_amount_exempt"] += tax_res["total_excluded"]
            else:
                totals["subtotal_amount_taxable"] += tax_res["total_excluded"]

            line_amounts[move] = {
                "value": self.company_id.currency_id.round(tax_res["total_included"]),
                "total_amount": self.company_id.currency_id.round(
                    tax_res["total_excluded"]
                ),
                "price_unit": tax_res["total_excluded"]
                / move.product_uom_qty,  # No rounding
                "wh_taxes": move_retentions,
                "exempt": not taxes and tax_res["total_excluded"] != 0.0,
            }
            if guide_price == "sale_order" and sale_line.discount:
                tax_res_disc = taxes.compute_all(
                    sale_line.price_unit,
                    currency=self.company_id.currency_id,
                    quantity=qty,
                    partner=self.partner_id,
                )
                line_amounts[move].update(
                    {
                        "price_unit": tax_res_disc["total_excluded"]
                        / move.product_uom_qty,  # No rounding
                        "discount": sale_line.discount,
                        "total_discount": float_repr(
                            self.company_id.currency_id.round(
                                tax_res_disc["total_excluded"]
                                * sale_line.discount
                                / 100
                            ),
                            0,
                        ),
                        "total_discount_fl": self.company_id.currency_id.round(
                            tax_res_disc["total_excluded"] * sale_line.discount / 100
                        ),
                    }
                )

        totals["vat_percent"] = max_vat_perc and float_repr(max_vat_perc, 2) or False
        retention_res = []
        for key in retentions:
            retention_res.append(
                {
                    "tax_code": key[0],
                    "tax_percent": key[1],
                    "tax_amount": retentions[key],
                }
            )
        return totals, retention_res, line_amounts
