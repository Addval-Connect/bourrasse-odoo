# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    client_order_date = fields.Date(string="Customer Reference Date", copy=False)

    def get_header_data(self):
        """get header data for invoice report"""
        report_name = ""
        if self.state in ["draft", "sent"]:
            report_name = "Presupuesto"
        if self.state in ["sale", "done"]:
            report_name = "Nota de Venta"
        if self.state == "cancel":
            report_name = "Nota de Venta Anulada"
        header_data = {
            "report_number": self.name,
            "report_name": report_name,
            "primary_color": self.company_id.primary_color,
            "header_address": self.company_id.partner_id,
            "company_logo": self.company_id.logo if self.company_id.logo else None,
            "company_name": self.company_id.partner_id.name,
            "company_activity": self.company_id.partner_id.l10n_cl_activity_description,
            "company_vat": self.company_id.partner_id._format_dotted_vat_cl(
                self.company_id.partner_id.vat
            )
            if self.company_id.partner_id.vat
            else None,
        }
        return header_data

    def get_invoice_data(self):
        """get information data for invoice report"""
        invoice_data = {
            "secondary_color": self.company_id.secondary_color,
            "order_date": self.client_order_date if self.client_order_date else None,
            "order_reference": self.client_order_ref if self.client_order_ref else None,
            "sale_representative": self.user_id.name,
            "company_name": self.partner_id.parent_name
            if self.partner_id.parent_name
            else self.partner_id.name,
            "company_vat": self.partner_id._format_dotted_vat_cl(self.partner_id.vat)
            if self.partner_id.vat
            else None,
            "latam_identification_type_id": True,
            "activity_description": self.partner_id.l10n_cl_activity_description,
            "address": self.partner_invoice_id,
            "shipping_address": self.partner_shipping_id,
            "payment_term": self.payment_term_id.name,
        }
        return invoice_data
