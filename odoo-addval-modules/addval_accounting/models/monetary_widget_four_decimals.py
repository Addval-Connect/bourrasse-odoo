# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from markupsafe import Markup as M
from odoo import _, api, fields, models


class MonetaryConverter(models.Model):
    """``monetary`` converter, has a mandatory option
    ``display_currency`` only if field is not of type Monetary.
    Otherwise, if we are in presence of a monetary field, the field definition must
    have a currency_field attribute set.

    Four decimal places are used for romating formatting and no rounding is applyed to the float value.

    .. note:: the monetary converter internally adds the qweb context to its
              options mapping, so that the context is available to callees.
              It's set under the ``_values`` key.
    """

    _name = "ir.qweb.field.monetary_four_decimals"
    _description = "Qweb Field Monetary four decimals"
    _inherit = "ir.qweb.field.monetary"

    @api.model
    def value_to_html(self, value, options):
        display_currency = options["display_currency"]

        if not isinstance(value, (int, float)):
            raise ValueError(_("The value send to monetary field is not a number."))

        # lang.format mandates a sprintf-style format. These formats are non-
        # minimal (they have a default fixed precision instead), and
        # lang.format will not set one by default. currency.round will not
        # provide one either. So we need to generate a precision value
        # (integer > 0) from the currency's rounding (a float generally < 1.0).
        fmt = "%.{0}f".format(4)

        if options.get("from_currency"):
            date = options.get("date") or fields.Date.today()
            company_id = options.get("company_id")
            if company_id:
                company = self.env["res.company"].browse(company_id)
            else:
                company = self.env.company
            value = options["from_currency"]._convert(
                value, display_currency, company, date
            )

        lang = self.user_lang()
        formatted_amount = (
            lang.format(
                # fmt, display_currency.round(value), grouping=True, monetary=True
                fmt,
                value,
                grouping=True,
                monetary=True,
            )
            .replace(r" ", "\N{NO-BREAK SPACE}")
            .replace(r"-", "-\N{ZERO WIDTH NO-BREAK SPACE}")
        )

        pre = post = ""
        if display_currency.position == "before":
            pre = "{symbol}\N{NO-BREAK SPACE}".format(
                symbol=display_currency.symbol or ""
            )
        else:
            post = "\N{NO-BREAK SPACE}{symbol}".format(
                symbol=display_currency.symbol or ""
            )

        if options.get("label_price") and lang.decimal_point in formatted_amount:
            sep = lang.decimal_point
            integer_part, decimal_part = formatted_amount.split(sep)
            integer_part += sep
            return M(
                '{pre}<span class="oe_currency_value">{0}</span><span class="oe_currency_value" style="font-size:0.5em">{1}</span>{post}'
            ).format(integer_part, decimal_part, pre=pre, post=post)

        return M('{pre}<span class="oe_currency_value">{0}</span>{post}').format(
            formatted_amount, pre=pre, post=post
        )
