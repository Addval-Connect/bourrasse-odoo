# -*- coding: utf-8 -*-
import base64
import re
from html import unescape

from lxml import etree
from odoo import _, models
from odoo.exceptions import UserError

L10N_CL_SII_REGIONAL_OFFICES_BY_LOCALITY = {
    "ARICA": "ARICA",
    "CAMARONES": "ARICA",
    "PUTRE": "ARICA",
    "GENERAL LAGOS": "ARICA",
    "IQUIQUE": "IQUIQUE",
    "PICA": "IQUIQUE",
    "POZO ALMONTE": "IQUIQUE",
    "HUARA": "IQUIQUE",
    "CAMINA": "IQUIQUE",
    "COLCHANE": "IQUIQUE",
    "ALTO HOSPICIO": "IQUIQUE",
    "ANTOFAGASTA": "ANTOFAGASTA",
    "MEJILLONES": "ANTOFAGASTA",
    "SIERRA GORDA": "ANTOFAGASTA",
    "CALAMA": "CALAMA",
    "SAN PEDRO DE ATACAMA": "CALAMA",
    "OLLAGUE": "CALAMA",
    "TOCOPILLA": "TOCOPILLA",
    "MARIA ELENA": "TOCOPILLA",
    "TALTAL": "TALTAL",
    "COPIAPO": "COPIAPÓ",
    "CALDERA": "COPIAPÓ",
    "TIERRA AMARILLA": "COPIAPÓ",
    "CHANARAL": "CHAÑARAL",
    "DIEGO DE ALMAGRO": "CHAÑARAL",
    "VALLENAR": "VALLENAR",
    "FREIRINA": "VALLENAR",
    "HUASCO": "VALLENAR",
    "ALTO DEL CARMEN": "VALLENAR",
    "LA SERENA": "LA SERENA",
    "LA HIGUERA": "LA SERENA",
    "PAIHUANO": "LA SERENA",
    "ANDACOLLO": "LA SERENA",
    "VICUNA": "LA SERENA",
    "OVALLE": "OVALLE",
    "MONTE PATRIA": "OVALLE",
    "PUNITAQUI": "OVALLE",
    "COMBARBALA": "OVALLE",
    "RIO HURTADO": "OVALLE",
    "ILLAPEL": "ILLAPEL",
    "SALAMANCA": "ILLAPEL",
    "LOS VILOS": "ILLAPEL",
    "CANELA": "ILLAPEL",
    "COMQUIMBO": "COQUIMBO",
    "VALPARAISO": "VALPARAÍSO",
    "CASABLANCA": "VALPARAÍSO",
    "JUAN FERNANDEZ": "VALPARAÍSO",
    "ISLA DE PASCUA": "VALPARAÍSO",
    "CONCON": "VIÑA DEL MAR",
    "QUINTERO": "VIÑA DEL MAR",
    "PUCHUNCAVI": "VIÑA DEL MAR",
    "VINA DEL MAR": "VIÑA DEL MAR",
    "LA LIGUA": "LA LIGUA",
    "PETORCA": "LA LIGUA",
    "CABILDO": "LA LIGUA",
    "ZAPALLAR": "LA LIGUA",
    "PAPUDO": "LA LIGUA",
    "SAN ANTONIO": "SAN ANTONIO",
    "SANTO DOMINGO": "SAN ANTONIO",
    "CARTAGENA": "SAN ANTONIO",
    "EL TABO": "SAN ANTONIO",
    "EL QUISCO": "SAN ANTONIO",
    "ALGARROBO": "SAN ANTONIO",
    "QUILLOTA": "QUILLOTA",
    "NOGALES": "QUILLOTA",
    "HIJUELAS": "QUILLOTA",
    "LA CALERA": "QUILLOTA",
    "LA CRUZ": "QUILLOTA",
    "LIMACHE": "QUILLOTA",
    "OLMUE": "QUILLOTA",
    "SAN FELIPE": "SAN FELIPE",
    "PANQUEHUE": "SAN FELIPE",
    "CATEMU": "SAN FELIPE",
    "PUTAENDO": "SAN FELIPE",
    "SANTA MARIA": "SAN FELIPE",
    "LLAY LLAY": "SAN FELIPE",
    "LOS ANDES": "LOS ANDES",
    "CALLE LARGA": "LOS ANDES",
    "SAN ESTEBAN": "LOS ANDES",
    "RINCONADA": "LOS ANDES",
    "VILLA ALEMANA": "VILLA ALEMANA",
    "QUILPUE": "VILLA ALEMANA",
    "RANCAGUA": "RANCAGUA",
    "MACHALI": "RANCAGUA",
    "GRANEROS": "RANCAGUA",
    "SAN FRANCISCO DE MOSTAZAL": "RANCAGUA",
    "DONIHUE": "RANCAGUA",
    "CODEGUA": "RANCAGUA",
    "RENGO": "RANCAGUA",
    "COLTAUCO": "RANCAGUA",
    "REQUINOA": "RANCAGUA",
    "OLIVAR": "RANCAGUA",
    "MALLOA": "RANCAGUA",
    "COINCO": "RANCAGUA",
    "QUINTA DE TILCOCO": "RANCAGUA",
    "SAN FERNANDO": "SAN FERNANDO",
    "CHIMBARONGO": "SAN FERNANDO",
    "NANCAGUA": "SAN FERNANDO",
    "PLACILLA": "SAN FERNANDO",
    "SANTA CRUZ": "SANTA CRUZ",
    "LOLOL": "SANTA CRUZ",
    "PALMILLA": "SANTA CRUZ",
    "PERALILLO": "SANTA CRUZ",
    "CHEPICA": "SANTA CRUZ",
    "PUMANQUE": "SANTA CRUZ",
    "SAN VICENTE": "SAN VICENTE TAGUA TAGUA",
    "LAS CABRAS": "SAN VICENTE TAGUA TAGUA",
    "PEUMO": "SAN VICENTE TAGUA TAGUA",
    "PICHIDEGUA": "SAN VICENTE TAGUA TAGUA",
    "PICHILEMU": "PICHILEMU",
    "PAREDONES": "PICHILEMU",
    "MARCHIGUE": "PICHILEMU",
    "LITUECHE": "PICHILEMU",
    "LA ESTRELLA": "PICHILEMU",
    "TALCA": "TALCA",
    "SAN CLEMENTE": "TALCA",
    "PELARCO": "TALCA",
    "RIO CLARO": "TALCA",
    "PENCAHUE": "TALCA",
    "MAULE": "TALCA",
    "CUREPTO": "TALCA",
    "SAN JAVIER": "TALCA",
    "LINARES": "LINARES",
    "YERBAS BUENAS": "LINARES",
    "COLBUN": "LINARES",
    "LONGAVI": "LINARES",
    "VILLA ALEGRE": "LINARES",
    "CONSTITUCION": "CONSTITUCIÓN",
    "EMPEDRADO": "CONSTITUCIÓN",
    "CAUQUENES": "CAUQUENES",
    "PELLUHUE": "CAUQUENES",
    "CHANCO": "CAUQUENES",
    "PARRAL": "PARRAL",
    "RETIRO": "PARRAL",
    "CURICO": "CURICÓ",
    "TENO": "CURICÓ",
    "ROMERAL": "CURICÓ",
    "MOLINA": "CURICÓ",
    "HUALANE": "CURICÓ",
    "SAGRADA FAMILIA": "CURICÓ",
    "LICANTEN": "CURICÓ",
    "VICHUQUEN": "CURICÓ",
    "RAUCO": "CURICÓ",
    "CONCEPCION": "CONCEPCIÓN",
    "CHIGUAYANTE": "CONCEPCIÓN",
    "SAN PEDRO DE LA PAZ": "CONCEPCIÓN",
    "PENCO": "CONCEPCIÓN",
    "HUALQUI": "CONCEPCIÓN",
    "FLORIDA": "CONCEPCIÓN",
    "TOME": "CONCEPCIÓN",
    "CORONEL": "CONCEPCIÓN",
    "LOTA": "CONCEPCIÓN",
    "SANTA JUANA": "CONCEPCIÓN",
    "ARAUCO": "CONCEPCIÓN",
    "CHILLAN": "CHILLÁN",
    "PINTO": "CHILLÁN",
    "EL CARMEN": "CHILLÁN",
    "SAN IGNACIO": "CHILLÁN",
    "PEMUCO": "CHILLÁN",
    "YUNGAY": "CHILLÁN",
    "BULNES": "CHILLÁN",
    "QUILLON": "CHILLÁN",
    "RANQUIL": "CHILLÁN",
    "PORTEZUELO": "CHILLÁN",
    "COELEMU": "CHILLÁN",
    "TREHUACO": "CHILLÁN",
    "QUIRIHUE": "CHILLÁN",
    "COBQUECURA": "CHILLÁN",
    "NINHUE": "CHILLÁN",
    "CHILLAN VIEJO": "CHILLÁN",
    "LOS ANGELES": "LOS ÁNGELES",
    "SANTA BARBARA": "LOS ÁNGELES",
    "LAJA": "LOS ÁNGELES",
    "QUILLECO": "LOS ÁNGELES",
    "NACIMIENTO": "LOS ÁNGELES",
    "NEGRETE": "LOS ÁNGELES",
    "MULCHEN": "LOS ÁNGELES",
    "QUILACO": "LOS ÁNGELES",
    "YUMBEL": "LOS ÁNGELES",
    "CABRERO": "LOS ÁNGELES",
    "SAN ROSENDO": "LOS ÁNGELES",
    "TUCAPEL": "LOS ÁNGELES",
    "ANTUCO": "LOS ÁNGELES",
    "ALTO BIO-BIO": "LOS ÁNGELES",
    "ALTO BIOBIO": "LOS ÁNGELES",
    "ALTO BIO BIO": "LOS ÁNGELES",
    "BIO-BIO": "LOS ÁNGELES",
    "BIOBIO": "LOS ÁNGELES",
    "BIO BIO": "LOS ÁNGELES",
    "SAN CARLOS": "SAN CARLOS",
    "SAN GREGORIO DE NINQUEN": "SAN CARLOS",
    "SAN NICOLAS": "SAN CARLOS",
    "SAN FABIAN DE ALICO": "SAN CARLOS",
    "TALCAHUANO": "TALCAHUANO",
    "HUALPEN": "TALCAHUANO",
    "LEBU": "LEBU",
    "CURANILAHUE": "LEBU",
    "LOS ALAMOS": "LEBU",
    "CANETE": "LEBU",
    "CONTULMO": "LEBU",
    "TIRUA": "LEBU",
    "TEMUCO": "TEMUCO",
    "VILCUN": "TEMUCO",
    "FREIRE": "TEMUCO",
    "CUNCO": "TEMUCO",
    "LAUTARO": "TEMUCO",
    "PERQUENCO": "TEMUCO",
    "GALVARINO": "TEMUCO",
    "NUEVA IMPERIAL": "TEMUCO",
    "CARAHUE": "TEMUCO",
    "PUERTO SAAVEDRA": "TEMUCO",
    "PITRUFQUEN": "TEMUCO",
    "GORBEA": "TEMUCO",
    "TOLTEN": "TEMUCO",
    "LONCOCHE": "TEMUCO",
    "MELIPEUCO": "TEMUCO",
    "TEODORO SCHMIDT": "TEMUCO",
    "PADRE LAS CASAS": "TEMUCO",
    "CHOLCHOL": "TEMUCO",
    "ANGOL": "ANGOL",
    "PUREN": "ANGOL",
    "LOS SAUCES": "ANGOL",
    "REINACO": "ANGOL",
    "COLLIPULLI": "ANGOL",
    "ERCILLA": "ANGOL",
    "VICTORIA": "VICTORIA",
    "TRAIGUEN": "VICTORIA",
    "LUMACO": "VICTORIA",
    "CURACAUTIN": "VICTORIA",
    "LONQUIMAY": "VICTORIA",
    "VILLARRICA": "VILLARRICA",
    "PUCON": "VILLARRICA",
    "CURARREHUE": "VILLARRICA",
    "VALDIVIA": "VALDIVIA",
    "MARIQUINA": "VALDIVIA",
    "LANCO": "LANCO",
    "MAFIL": "VALDIVIA",
    "CORRAL": "VALDIVIA",
    "LOS LAGOS": "VALDIVIA",
    "PAILLACO": "VALDIVIA",
    "PANGUIPULLI": "PANGUIPULLI",
    "LA UNION": "LA UNIÓN",
    "FUTRONO": "VALDIVIA",
    "RIO BUENO": "LA UNIÓN",
    "LAGO RANCO": "LA UNIÓN",
    "PUERTO MONTT": "PUERTO MONTT",
    "CALBUCO": "PUERTO MONTT",
    "MAULLIN": "PUERTO MONTT",
    "LOS MUERMOS": "PUERTO MONTT",
    "HUALAIHUE": "PUERTO MONTT",
    "PUERTO VARAS": "PUERTO VARAS",
    "COCHAMO": "PUERTO VARAS",
    "FRESIA": "PUERTO VARAS",
    "LLANQUIHUE": "PUERTO VARAS",
    "FRUTILLAR": "PUERTO VARAS",
    "ANCUD": "ANCUD",
    "QUEMCHI": "ANCUD",
    "OSORNO": "OSORNO",
    "PUYEHUE": "OSORNO",
    "PURRANQUE": "OSORNO",
    "RIO NEGRO": "OSORNO",
    "SAN PABLO": "OSORNO",
    "SAN JUAN DE LA COSTA": "OSORNO",
    "PUERTO OCTAY": "OSORNO",
    "CASTRO": "CASTRO",
    "CURACO DE VÉLEZ": "CASTRO",
    "CHOCHI": "CASTRO",
    "DALCAHUE": "CASTRO",
    "PUQUELDON": "CASTRO",
    "QUEILEN": "CASTRO",
    "QUELLON": "CASTRO",
    "CHAITEN": "CHAITÉN",
    "PALENA": "CHAITÉN",
    "FUTALEUFU": "CHAITÉN",
    "COYHAIQUE": "COYHAIQUE",
    "RIO IBANEZ": "COYHAIQUE",
    "O`HIGGINS": "COCHRANE",
    "OHIGGINS": "COCHRANE",
    "O HIGGINS": "COCHRANE",
    "TORTEL": "COCHRANE",
    "AYSEN": "AYSÉN",
    "CISNES": "AYSÉN",
    "LAGO VERDE": "AYSÉN",
    "GUAITECAS": "AYSÉN",
    "CHILE CHICO": "CHILE CHICO",
    "COCHRANE": "COCHRANE",
    "GUADAL": "COCHRANE",
    "PUERTO BELTRAND": "COCHRANE",
    "PUNTA ARENAS": "PUNTA ARENAS",
    "RIO VERDE": "PUNTA ARENAS",
    "SAN GREGORIO": "PUNTA ARENAS",
    "LAGUNA BLANCA": "PUNTA ARENAS",
    "CABO DE HORNOS": "PUNTA ARENAS",
    "PUERTO NATALES": "PUERTO NATALES",
    "TORRES DEL PAINE": "PUERTO NATALES",
    "PORVENIR": "PORVENIR",
    "PRIMAVERA": "PORVENIR",
    "TIMAUKEL": "PORVENIR",
    "INDEPENDENCIA": "SANTIAGO NORTE",
    "RECOLETA": "SANTIAGO NORTE",
    "HUECHURABA": "SANTIAGO NORTE",
    "CONCHALI": "SANTIAGO NORTE",
    "QUILICURA": "SANTIAGO NORTE",
    "COLINA": "SANTIAGO NORTE",
    "LAMPA": "SANTIAGO NORTE",
    "TILTIL": "SANTIAGO NORTE",
    "SANTIAGO": "SANTIAGO CENTRO",
    "CERRO NAVIA": "SANTIAGO PONIENTE",
    "CURACAVI": "SANTIAGO PONIENTE",
    "ESTACION CENTRAL": "SANTIAGO PONIENTE",
    "LO PRADO": "SANTIAGO PONIENTE",
    "PUDAHUEL": "SANTIAGO PONIENTE",
    "QUINTA NORMAL": "SANTIAGO PONIENTE",
    "RENCA": "SANTIAGO PONIENTE",
    "MELIPILLA": "MELIPILLA",
    "SAN PEDRO": "MELIPILLA",
    "ALHUE": "MELIPILLA",
    "MARIA PINTO": "MELIPILLA",
    "MAIPU": "MAIPÚ",
    "CERRILLOS": "MAIPÚ",
    "PADRE HURTADO": "MAIPÚ",
    "PENAFLOR": "MAIPÚ",
    "TALAGANTE": "MAIPÚ",
    "EL MONTE": "MAIPÚ",
    "ISLA DE MAIPO": "MAIPÚ",
    "LAS CONDES": "SANTIAGO ORIENTE",
    "VITACURA": "SANTIAGO ORIENTE",
    "LO BARNECHEA": "SANTIAGO ORIENTE",
    "NUNOA": "ÑUÑOA",
    "LA REINA": "ÑUÑOA",
    "MACUL": "ÑUÑOA",
    "PENALOLEN": "ÑUÑOA",
    "PROVIDENCIA": "PROVIDENCIA",
    "SAN MIGUEL": "SANTIAGO SUR",
    "LA CISTERNA": "SANTIAGO SUR",
    "SAN JOAQUIN": "SANTIAGO SUR",
    "PEDRO AGUIRRE CERDA": "SANTIAGO SUR",
    "LO ESPEJO": "SANTIAGO SUR",
    "LA GRANJA": "SANTIAGO SUR",
    "LA PINTANA": "SANTIAGO SUR",
    "SAN RAMON": "SANTIAGO SUR",
    "LA FLORIDA": "LA FLORIDA",
    "PUENTE ALTO": "LA FLORIDA",
    "PIRQUE": "LA FLORIDA",
    "SAN JOSE DE MAIPO": "LA FLORIDA",
    "SAN BERNARDO": "SAN BERNARDO",
    "CALERA DE TANGO": "SAN BERNARDO",
    "EL BOSQUE": "SAN BERNARDO",
    "BUIN": "BUIN",
    "PAINE": "BUIN",
}


class StateID(object):
    def __init__(self, name=""):
        self.name = name


class CountryID(object):
    def __init__(self, name=""):
        self.name = name


class HeaderAddress:
    def __init__(
        self,
        street="",
        street2="",
        city="",
        state_id=StateID(),
        country_id=CountryID(),
        phone="",
        website="",
        email="",
    ):
        self.street = street
        self.street2 = street2
        self.city = city
        self.state_id = state_id
        self.country_id = country_id
        self.phone = phone
        self.website = website
        self.email = email


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_mass_validate(self):
        return {
            "name": _("Bulk Validate"),
            "res_model": "validate.account.move",
            "view_mode": "form",
            "target": "new",
            "type": "ir.actions.act_window",
            "context": {
                "active_model": "account.move",
                "active_ids": self.ids,
            },
        }

    def action_mass_print(self):
        attachment_ids = []
        for rec in self:
            report = self.env.ref("account.account_invoices")._render_qweb_pdf(rec.ids)
            partner_name = "unknown"
            names = rec.partner_id.name_get()
            if names:
                partner_name = names[0][1]
            filename = f"{rec.l10n_latam_document_number}_{partner_name}.pdf"
            invoice_pdfs = self.env["ir.attachment"].create(
                {
                    "name": filename,
                    "type": "binary",
                    "datas": base64.b64encode(report[0]),
                    "res_model": "account.move",
                    "res_id": rec.id,
                    "mimetype": "application/pdf",
                }
            )
            attachment_ids.append(invoice_pdfs.id)
        return {
            "type": "ir.actions.act_url",
            "url": "/print/invoices?attachment_ids=%(attachment_ids)s"
            % {"attachment_ids": ",".join(str(x) for x in attachment_ids)},
        }

    def get_tags_from_xml(self, tags):
        """get tag from xml"""
        if not self.l10n_cl_dte_file:
            return {}
        matches = {}
        xml_data = (
            base64.b64decode(self.l10n_cl_dte_file.datas)
            .decode("iso-8859-1")
            .replace("\n", " ")
        )
        for label, tag in tags.items():
            regex = r"<" + re.escape(tag) + r">.*</" + re.escape(tag) + r">"
            search_data = re.search(regex, xml_data)
            if not search_data:
                continue
            match_data = (
                search_data.group(0).replace(f"<{tag}>", "").replace(f"</{tag}>", "")
            )
            matches.update({label: unescape(match_data)})
        return matches

    def get_header_data(self):
        """get header data for invoice report"""
        regional_office_dict = dict(
            self.company_id._fields["l10n_cl_sii_regional_office"].selection
        )
        header_data = {
            "report_number": self.l10n_latam_document_number,
            "report_name": self.l10n_latam_document_type_id.name,
            "primary_color": self.company_id.primary_color,
        }
        if self.move_type.startswith("in_"):
            value_tags = {
                "company_name": "RznSoc",
                "company_vat": "RUTEmisor",
                "company_activity": "GiroEmis",
                "address": "DirOrigen",
                "locality": "CmnaOrigen",
                "city": "CiudadOrigen",
                "phone": "FonoOrigen",
                "email": "CorreoEmisor",
                "website": "Web",
            }
            header_data.update(
                {
                    # "header_address": self.partner_id,
                    "company_logo": self.partner_id.image_1920
                    if self.partner_id.image_1920
                    else None,
                    "company_name": self.partner_id.parent_name
                    if self.partner_id.parent_name
                    else self.partner_id.name,
                    "company_activity": self.partner_id.l10n_cl_activity_description
                    if self.partner_id.l10n_cl_activity_description
                    else None,
                    "company_vat": self.partner_id._format_dotted_vat_cl(
                        self.partner_id.vat
                    )
                    if self.partner_id.vat
                    else None,
                }
            )
            missing_tags = {
                key: value
                for key, value in value_tags.items()
                if not header_data.get(key)
            }
            if missing_tags is None:
                return header_data
            data_from_xml = self.get_tags_from_xml(missing_tags)  # type: ignore
            header_address = HeaderAddress(
                street=data_from_xml.get("address", ""),
                street2=data_from_xml.get("locality", ""),
                city=data_from_xml.get("city", ""),
                country_id=CountryID(
                    name="Chile" if data_from_xml.get("address") else ""
                ),
                phone=data_from_xml.get("phone", ""),
                website=data_from_xml.get("website", ""),
                email=data_from_xml.get("email", ""),
            )
            company_vat = (
                self.partner_id._format_dotted_vat_cl(data_from_xml.get("company_vat"))
                if data_from_xml.get("company_vat")
                else None
            )
            regional_office = L10N_CL_SII_REGIONAL_OFFICES_BY_LOCALITY.get(
                data_from_xml.get("locality", "").strip().upper(), None
            )
            header_data.update(
                {
                    "header_address": header_address,
                    "company_name": data_from_xml.get(
                        "company_name", header_data.get("company_name", "")
                    ),
                    "company_vat": header_data.get("company_vat", company_vat),
                    "company_activity": data_from_xml.get(
                        "company_activity", header_data.get("company_activity", "")
                    ),
                    "regional_office": regional_office,
                }
            )
            return header_data
        header_data.update(
            {
                "header_address": self.company_id.partner_id,
                "company_logo": self.company_id.logo if self.company_id.logo else None,
                "company_name": self.company_id.partner_id.name,
                "company_activity": self.company_id.partner_id.l10n_cl_activity_description,
                "company_vat": self.company_id.partner_id._format_dotted_vat_cl(
                    self.company_id.partner_id.vat
                )
                if self.company_id.partner_id.vat
                else None,
                "regional_office": regional_office_dict.get(
                    self.company_id.l10n_cl_sii_regional_office, None
                ),
            }
        )
        return header_data

    def get_invoice_data(self):
        """get information data for invoice report"""
        invoice_data = {
            "secondary_color": self.company_id.secondary_color,
            "invoice_date": self.invoice_date,
            "date_due": self.invoice_date_due,
            "payment_term": self.invoice_payment_term_id.name,
            "incoterm": self.invoice_incoterm_id.name,
        }
        if self.move_type.startswith("in_"):
            invoice_data.update(
                {
                    "company_name": self.company_id.partner_id.name,
                    "company_vat": self.company_id.partner_id._format_dotted_vat_cl(
                        self.company_id.partner_id.vat
                    )
                    if self.company_id.partner_id.vat
                    else None,
                    "latam_identification_type_id": self.company_id.partner_id.l10n_latam_identification_type_id,
                    "activity_description": self.company_id.partner_id.l10n_cl_activity_description
                    or self.company_id.commercial_partner_id.l10n_cl_activity_description,
                    "address": self.company_id.partner_id,
                }
            )
            return invoice_data
        invoice_data.update(
            {
                "company_name": self.partner_id.parent_name
                if self.partner_id.parent_name
                else self.partner_id.name,
                "company_vat": self.partner_id._format_dotted_vat_cl(
                    self.partner_id.vat
                )
                if self.partner_id.vat
                else None,
                "latam_identification_type_id": self.partner_id.l10n_latam_identification_type_id,
                "activity_description": self.partner_id.l10n_cl_activity_description
                or self.commercial_partner_id.l10n_cl_activity_description,
                "address": self.partner_id,
            }
        )
        return invoice_data

    def get_barcode_from_xml(self):
        """get barcode from xml"""
        ted_data = r"<TED.*</TED>"
        xml_data = (
            base64.b64decode(self.l10n_cl_dte_file.datas)
            .decode("iso-8859-1")
            .replace("\n", " ")
            if self.l10n_cl_dte_file
            else "No Data"
        )
        search_data = re.search(ted_data, xml_data)
        match_data = search_data.group(0) if search_data else None
        barcode_data = (
            etree.tostring(
                etree.fromstring(
                    match_data, parser=etree.XMLParser(remove_blank_text=True)
                )
            )
            if match_data
            else None
        )
        return barcode_data


# class AccountMoveReversal(models.TransientModel):
#     _inherit = "account.move.reversal"

#     # Default set 'Credit Notes' journal
#     def default_get(self, fields):
#         res = super(AccountMoveReversal, self).default_get(fields)
#         if self._context.get("is_from_credit_note"):
#             res["journal_id"] = self.env.ref("addval_accounting.credit_note_journal").id
#         return res


class ValidateAccountMove(models.TransientModel):
    _inherit = "validate.account.move"

    # Validation: Bulk validate is apply only on unpaid invoices.
    def validate_move(self):
        selected_ids = self._context.get("active_ids")
        AccountMoves = (
            self.env["account.move"]
            .browse(selected_ids)
            .filtered(lambda x: x.payment_state != "not_paid")
        )
        if AccountMoves:
            invoice_numbers = [rec + "\n" for rec in AccountMoves.mapped("name")]
            raise UserError(
                _(
                    "Bulk validate is apply only on unpaid invoices. Please remove below Invoices. \n%s"
                    % "".join(invoice_numbers)
                )
            )
        return super(ValidateAccountMove, self).validate_move()
