# -*- coding: utf-8 -*-
import logging
import xml.etree.ElementTree as ET

from odoo import _, fields, models
from odoo.tests import Form

_logger = logging.getLogger(__name__)


class FetchmailServer(models.Model):
    _inherit = "fetchmail.server"

    def _get_dte_purchase_journal(self, company_id):
        _logger.info("Looking for default purchase journal for company: %s", company_id)

        """Overload of original method to return the purchase journal,
        giving priority to those with read_dte=True"""
        journals = self.env["account.journal"].search(
            [
                ("type", "=", "purchase"),
                ("l10n_latam_use_documents", "=", True),
                ("company_id", "=", company_id),
                ("read_dte", "=", True),
            ],
            limit=1,
        )

        if not journals:
            journals = self.env["account.journal"].search(
                [
                    ("type", "=", "purchase"),
                    ("l10n_latam_use_documents", "=", True),
                    ("company_id", "=", company_id),
                ],
                limit=1,
            )
            _logger.info(
                "No DTE priority journal found, selecting journal: '%s' for company: %s",
                journals,
                company_id,
            )
            return journals
        _logger.info(
            "DTE priority journal: '%s' found for company: %s", journals, company_id
        )
        return journals

    # def _get_vendor_product(self, product_code, product_name, company_id, partner_id):
    #     """
    #     This tries to match products specified in the vendor bill with current products in database.
    #     Criteria to attempt a match with existent products:
    #     1) check if product_code in the supplier info is present (if partner_id is established)
    #     2) if (1) fails, check if product supplier info name is present (if partner_id is established)
    #     3) if (1) and (2) fail, check product default_code
    #     4) if 3 previous criteria fail, check product name, and return false if fails
    #     """
    #     _logger.info(
    #         "Looking vendor product for '%s', code '%s' for company_id:  '%s' and partner_id: '%s'",
    #         product_name,
    #         product_code,
    #         company_id,
    #         partner_id,
    #     )
    #     if partner_id:
    #         supplier_info_domain = [
    #             ("name", "=", partner_id),
    #             ("company_id", "in", [company_id, False]),
    #         ]
    #         if product_code:
    #             # 1st criteria
    #             supplier_info_domain.append(("product_code", "=", product_code))
    #         else:
    #             # 2nd criteria
    #             supplier_info_domain.append(("product_name", "=", product_name))
    #         supplier_info = (
    #             self.env["product.supplierinfo"]
    #             .sudo()
    #             .search(supplier_info_domain, limit=1)
    #         )
    #         if supplier_info:
    #             _logger.info(
    #                 "Found product: '%s', for suplier: '%s'",
    #                 supplier_info.product_id,
    #                 supplier_info,
    #             )
    #             return supplier_info.product_id
    #     # 3rd criteria
    #     if product_code:
    #         product = (
    #             self.env["product.product"]
    #             .sudo()
    #             .search(
    #                 [
    #                     "|",
    #                     ("default_code", "=", product_code),
    #                     ("barcode", "=", product_code),
    #                     ("company_id", "in", [company_id, False]),
    #                 ],
    #                 limit=1,
    #             )
    #         )
    #         if product:
    #             _logger.info(
    #                 "Found product: '%s', matching code: '%s'", product, product_code
    #             )
    #             return product
    #     # 4th criteria
    #     product = (
    #         self.env["product.product"]
    #         .sudo()
    #         .search(
    #             [
    #                 ("company_id", "in", [company_id, False]),
    #                 ("name", "ilike", product_name),
    #             ],
    #             limit=1,
    #         )
    #     )
    #     _logger.info("Found product: '%s', matching name: '%s'", product, product_name)
    #     return product

    # def _get_reference_document_type(self, xml_content):
    #     return xml_content.findtext(".//ns0:TpoDocRef", namespaces=XML_NAMESPACES)

    # def _get_reference_document_number(self, xml_content):
    #     return xml_content.findtext(".//ns0:FolioRef", namespaces=XML_NAMESPACES)

    # def _get_partner_sii_regional_office(self, xml_content):
    #     return xml_content.findtext(".//ns0:CdgSIISucur", namespaces=XML_NAMESPACES)

    # def _get_sii_barcode(self, xml_content):
    #     return ET.tostring(xml_content.xpath(".//ns0:TED", namespaces=XML_NAMESPACES))

    # def _get_invoice_form(
    #     self,
    #     company_id,
    #     partner,
    #     default_move_type,
    #     from_address,
    #     dte_xml,
    #     document_number,
    #     document_type,
    #     msgs,
    # ):
    #     """
    #     This method creates a draft vendor bill from the attached xml in the incoming email.
    #     """
    #     with Form(
    #         self.env["account.move"].with_context(
    #             default_move_type=default_move_type,
    #             allowed_company_ids=[company_id],
    #             account_predictive_bills_disable_prediction=True,
    #         )
    #     ) as invoice_form:
    #         invoice_form.partner_id = partner
    #         invoice_form.invoice_source_email = from_address
    #         invoice_date = dte_xml.findtext(".//ns0:FchEmis", namespaces=XML_NAMESPACES)
    #         if invoice_date is not None:
    #             invoice_form.invoice_date = fields.Date.from_string(invoice_date)
    #         # Set the date after invoice_date to avoid the onchange
    #         invoice_form.date = fields.Date.context_today(
    #             self.with_context(tz="America/Santiago")
    #         )

    #         invoice_date_due = dte_xml.findtext(
    #             ".//ns0:FchVenc", namespaces=XML_NAMESPACES
    #         )
    #         if invoice_date_due is not None:
    #             invoice_form.invoice_date_due = fields.Date.from_string(
    #                 invoice_date_due
    #             )

    #         # Link purchase_orde to invoice if reference is of type 801 and purchase_orde exists
    #         reference_document_type = self._get_reference_document_type(dte_xml)
    #         if reference_document_type == "801":
    #             purchase_order_prefix = (
    #                 self.env["ir.sequence"]
    #                 .search(["code", "=", "purchase.order"])
    #                 .prefix
    #             )
    #             reference_document_number = (
    #                 purchase_order_prefix + self._get_reference_document_number(dte_xml)
    #             )
    #             purchase_order = self.env["purchase.order"].search(
    #                 [("name", "=", reference_document_number)], limit=1
    #             )
    #             invoice_form.purchase_id = purchase_order

    #         partner_sii_regional_office = self._get_partner_sii_regional_office(dte_xml)
    #         if partner_sii_regional_office:
    #             invoice_form.partner_sii_regional_office = partner_sii_regional_office
    #         l10n_cl_sii_barcode = self._get_sii_barcode(dte_xml)
    #         if l10n_cl_sii_barcode:
    #             invoice_form.l10n_cl_sii_barcode = l10n_cl_sii_barcode

    #         journal = self._get_dte_purchase_journal(company_id)
    #         if journal:
    #             invoice_form.journal_id = journal
    #         currency = self._get_dte_currency(dte_xml)
    #         if currency:
    #             invoice_form.currency_id = currency

    #         invoice_form.l10n_latam_document_type_id = document_type
    #         invoice_form.l10n_latam_document_number = document_number
    #         for invoice_line in self._get_dte_lines(dte_xml, company_id, partner.id):
    #             price_unit = invoice_line.get("price_unit")
    #             with invoice_form.invoice_line_ids.new() as invoice_line_form:
    #                 invoice_line_form.product_id = invoice_line.get(
    #                     "product", self.env["product.product"]
    #                 )
    #                 invoice_line_form.name = invoice_line.get("name")
    #                 invoice_line_form.quantity = invoice_line.get("quantity")
    #                 invoice_line_form.price_unit = price_unit
    #                 invoice_line_form.discount = invoice_line.get("discount", 0)

    #                 if not invoice_line.get("default_tax"):
    #                     invoice_line_form.tax_ids.clear()
    #                 for tax in invoice_line.get("taxes", []):
    #                     invoice_line_form.tax_ids.add(tax)
    #         for reference_line in self._get_invoice_references(dte_xml):
    #             if not self._is_valid_reference_doc_type(
    #                 reference_line.get("l10n_cl_reference_doc_type_selection")
    #             ):
    #                 msgs.append(
    #                     _(
    #                         "There is an unidentified reference in this invoice:<br/>"
    #                         "<li>Origin: %(origin_doc_number)s<li/>"
    #                         "<li>Reference Code: %(reference_doc_code)s<li/>"
    #                         "<li>Doc Type: %(l10n_cl_reference_doc_type_selection)s<li/>"
    #                         "<li>Reason: %(reason)s<li/>"
    #                         "<li>Date:%(date)s"
    #                     )
    #                     % reference_line
    #                 )
    #                 continue
    #             with invoice_form.l10n_cl_reference_ids.new() as reference_line_form:
    #                 reference_line_form.origin_doc_number = reference_line[
    #                     "origin_doc_number"
    #                 ]
    #                 reference_line_form.reference_doc_code = reference_line[
    #                     "reference_doc_code"
    #                 ]
    #                 reference_line_form.l10n_cl_reference_doc_type_selection = (
    #                     reference_line["l10n_cl_reference_doc_type_selection"]
    #                 )
    #                 reference_line_form.reason = reference_line["reason"]
    #                 reference_line_form.date = reference_line["date"]

    # return invoice_form, msgs
