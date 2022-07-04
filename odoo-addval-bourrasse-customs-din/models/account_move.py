# -*- coding: utf-8 -*-

from odoo import _, models
from odoo.exceptions import ValidationError

SII_VAT = "60805000-0"
SER_NA_AD_VAT = "60804000-5"


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_l10n_latam_documents_domain(self):
        self.ensure_one()
        if (
            self.journal_id.company_id.account_fiscal_country_id
            != self.env.ref("base.cl")
            or not self.journal_id.l10n_latam_use_documents
        ):
            return super()._get_l10n_latam_documents_domain()
        if self.journal_id.type == "sale":
            if self.move_type == "out_refund":
                internal_types_domain = ("internal_type", "=", "credit_note")
            else:
                internal_types_domain = (
                    "internal_type",
                    "in",
                    ["invoice", "debit_note"],
                )
            domain = [("country_id.code", "=", "CL"), internal_types_domain]
            if self.company_id.partner_id.l10n_cl_sii_taxpayer_type == "1":
                domain += [
                    ("code", "!=", "71")
                ]  # Companies with VAT Affected doesn't have "Boleta de honorarios Electrónica"
            return domain
        if self.move_type == "in_refund":
            internal_types_domain = ("internal_type", "=", "credit_note")
        else:
            internal_types_domain = (
                "internal_type",
                "in",
                ["invoice", "debit_note", "credit_note", "invoice_in"],
            )
        domain = [
            ("country_id.code", "=", "CL"),
            internal_types_domain,
        ]
        if (
            self.partner_id.l10n_cl_sii_taxpayer_type == "1"
            and self.partner_id_vat not in [SII_VAT, SER_NA_AD_VAT]
        ):
            domain += [("code", "not in", ["39", "70", "71", "914", "911"])]
        elif (
            self.partner_id.l10n_cl_sii_taxpayer_type == "1"
            and self.partner_id_vat in [SII_VAT, SER_NA_AD_VAT]
        ):
            domain += [("code", "not in", ["39", "70", "71"])]
            if self.move_type == "in_invoice":
                domain += [("internal_type", "!=", "credit_note")]
        elif self.partner_id.l10n_cl_sii_taxpayer_type == "2":
            domain += [("code", "in", ["70", "71", "56", "61"])]
        elif self.partner_id.l10n_cl_sii_taxpayer_type == "3":
            domain += [("code", "in", ["35", "38", "39", "41", "56", "61"])]
        elif (
            not self.partner_id.l10n_cl_sii_taxpayer_type
            or self.partner_id.country_id != self.env.ref("base.cl")
            or self.partner_id.l10n_cl_sii_taxpayer_type == "4"
        ):
            domain += [("code", "in", [])]
        return domain

    def _check_document_types_post(self):
        for rec in self.filtered(
            lambda r: r.company_id.account_fiscal_country_id.code == "CL"
            and r.journal_id.type in ["sale", "purchase"]
        ):
            tax_payer_type = rec.partner_id.l10n_cl_sii_taxpayer_type
            vat = rec.partner_id.vat
            country_id = rec.partner_id.country_id
            latam_document_type_code = rec.l10n_latam_document_type_id.code
            if (not tax_payer_type or not vat) and (
                country_id.code == "CL"
                and latam_document_type_code
                and latam_document_type_code not in ["35", "38", "39", "41"]
            ):
                raise ValidationError(
                    _(
                        "Tax payer type and vat number are mandatory for this type of "
                        "document. Please set the current tax payer type of this customer"
                    )
                )
            if (
                rec.journal_id.type == "sale"
                and rec.journal_id.l10n_latam_use_documents
            ):
                if country_id.code != "CL":
                    if not (
                        (
                            tax_payer_type == "4"
                            and latam_document_type_code in ["110", "111", "112"]
                        )
                        or (
                            tax_payer_type == "3"
                            and latam_document_type_code in ["39", "41", "61", "56"]
                        )
                    ):
                        raise ValidationError(
                            _(
                                "Document types for foreign customers must be export type (codes 110, 111 or 112) or you \
                            should define the customer as an end consumer and use receipts (codes 39 or 41)"
                            )
                        )
            if (
                rec.journal_id.type == "purchase"
                and rec.journal_id.l10n_latam_use_documents
            ):
                if (
                    vat not in [SII_VAT, SER_NA_AD_VAT]
                    and latam_document_type_code == "914"
                ):
                    raise ValidationError(
                        _(
                            "The DIN document is intended to be used only with RUT 60805000-0 or 60804000-5"
                            " (Tesorería General de La República) or (Servicio Nacional de Aduanas)"
                        )
                    )
                if not tax_payer_type or not vat:
                    if country_id.code == "CL" and latam_document_type_code not in [
                        "35",
                        "38",
                        "39",
                        "41",
                    ]:
                        raise ValidationError(
                            _(
                                "Tax payer type and vat number are mandatory for this type of "
                                "document. Please set the current tax payer type of this supplier"
                            )
                        )
                if tax_payer_type == "2" and latam_document_type_code not in [
                    "70",
                    "71",
                    "56",
                    "61",
                ]:
                    raise ValidationError(
                        _(
                            "The tax payer type of this supplier is incorrect for the selected type"
                            " of document."
                        )
                    )
                if tax_payer_type in ["1", "3"]:
                    if latam_document_type_code in ["70", "71"]:
                        raise ValidationError(
                            _(
                                "The tax payer type of this supplier is not entitled to deliver "
                                "fees documents"
                            )
                        )
                    if latam_document_type_code in ["110", "111", "112"]:
                        raise ValidationError(
                            _(
                                "The tax payer type of this supplier is not entitled to deliver "
                                "imports documents"
                            )
                        )
                if tax_payer_type == "4" or country_id.code != "CL":
                    raise ValidationError(
                        _(
                            "You need a journal without the use of documents for foreign "
                            "suppliers"
                        )
                    )
