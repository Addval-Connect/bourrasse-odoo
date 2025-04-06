# -*- coding: utf-8 -*-
import base64
import re
from html import unescape

from lxml import etree
from odoo import _, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def get_header_data(self):
        """get header data for invoice report"""
        regional_office_dict = dict(
            self.company_id._fields["l10n_cl_sii_regional_office"].selection
        )
        report_name = ""
        if self.state in ["draft", "sent", "to approve"]:
            report_name = "Pedido de Compra"
        if self.state in ["purchase", "done"]:
            report_name = "Orden de Compra"
        if self.state == "cancel":
            report_name = "Orden de Compra Anulada"
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
            # "regional_office": regional_office_dict.get(
            #     self.company_id.l10n_cl_sii_regional_office, None
            # ),
        }
        return header_data

    def get_invoice_data(self):
        """get information data for invoice report"""
        invoice_data = {
            "secondary_color": self.company_id.secondary_color,
            "order_date": self.date_order if self.date_order else None,
            "order_reference": self.partner_ref,
            "order_representative": self.user_id.name,
            "incoterm": self.incoterm_id.code,
            "company_name": self.partner_id.parent_name
            if self.partner_id.parent_name
            else self.partner_id.name,
            "company_vat": self.partner_id._format_dotted_vat_cl(self.partner_id.vat)
            if self.partner_id.vat
            else None,
            "latam_identification_type_id": True,
            "activity_description": self.partner_id.l10n_cl_activity_description,
            "address": self.partner_id,
            "shipping_address": self.dest_address_id if self.dest_address_id else None,
            "payment_term": self.payment_term_id.name,
        }
        return invoice_data
