# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import zipfile

from odoo.http import request, route, Controller, content_disposition
from datetime import datetime
try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO


class CustomerInvoices(Controller):

    @route(["/print/invoices"], type='http', auth='user')
    def print_customer_invoices(self, attachment_ids='', **post):
        if attachment_ids:
            ids = [int(s) for s in attachment_ids.split(',')]
            attachment_ids = request.env['ir.attachment'].browse(ids)
            file_dict = {}
            for attachment_id in attachment_ids:
                file_store_fname = attachment_id.store_fname
                if file_store_fname:
                    filename = attachment_id.name
                    filepath = attachment_id._full_path(file_store_fname)
                    file_dict["%s:%s" % (file_store_fname, filename)] = dict(path=filepath, name=filename)
            zip_filename = f"Invoices_{datetime.now()}.zip"
            bytes_io = BytesIO()
            zip_file = zipfile.ZipFile(bytes_io, "w", zipfile.ZIP_DEFLATED)
            for info in file_dict.values():
                zip_file.write(info["path"], info["name"])
            zip_file.close()
            attachment_ids.unlink()

        return request.make_response(bytes_io.getvalue(),
                                     headers=[('Content-Type', 'application/x-zip-compressed'),
                                              ('Content-Disposition', content_disposition(zip_filename))])