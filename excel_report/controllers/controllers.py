# -*- coding: utf-8 -*-

import json

from odoo import http
from odoo.http import content_disposition, request
from odoo.tools.safe_eval import safe_eval
from werkzeug.urls import url_decode
# from odoo.addons.web.controllers import ReportController
from odoo.addons.web.controllers.report import ReportController


class ReportControllerExcel(ReportController):
    @http.route([
        '/report/<converter>/<reportname>',
        '/report/<converter>/<reportname>/<docids>',
    ], type='http', auth='user', website=True)
    def report_routes(self, reportname, docids=None, converter=None, **data):
        if converter == 'excel':
            report = request.env['ir.actions.report'].search([
                ('report_name', '=', reportname)
            ], limit=1)

            if not report:
                return request.not_found()

            context = dict(request.env.context)
            data_new = dict(data)
            docids_new = None

            if docids:
                docids_new = [int(i) for i in docids.split(',')]

            # Handle options data
            if data_new.get('options'):
                data_new.update(json.loads(data_new.pop('options')))

            # Handle context data - Add null check and improved error handling
            if data_new.get('context') and data_new['context']:
                try:
                    context_data = json.loads(data_new['context'])
                    if isinstance(context_data, dict):
                        data_new['context'] = context_data
                        context.update(context_data)
                    else:
                        data_new['context'] = {}
                except (json.JSONDecodeError, TypeError):
                    # If context parsing fails, use empty dict
                    data_new['context'] = {}
            else:
                data_new['context'] = {}

            # Add model information to data for render_excel method
            if report.model:
                data_new['model'] = report.model

            text, file_type = report.with_context(context).render_excel(docids_new, data=data_new)

            # Set appropriate content type based on file type
            content_type_map = {
                'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'pdf': 'application/pdf',
                'ods': 'application/vnd.oasis.opendocument.spreadsheet',
                'odt': 'application/vnd.oasis.opendocument.text',
                'html': 'text/html'
            }

            content_type = content_type_map.get(file_type, 'application/vnd.ms-excel')
            texthttpheaders = [('Content-Type', content_type), ('Content-Length', len(text))]

            return request.make_response(text, headers=texthttpheaders)

        return super(ReportControllerExcel, self).report_routes(reportname, docids, converter, **data)

    @http.route(['/report/download'], type='http', auth="user")
    def report_download(self, data, context=None):
        """This function is used by 'action_manager_report.js' in order to trigger the download of
        a pdf/controller report.

        :param data: a javascript array JSON.stringified containg report internal url ([0]) and
        type [1]
        :returns: Response with a filetoken cookie and an attachment header
        """
        requestcontent = json.loads(data)
        url, type = requestcontent[0], requestcontent[1]
        reportname = '???'
        if type in ['excel']:
            converter = 'excel'  # if type == 'qweb-pdf' else 'text'
            extension = 'xlsx'  # if type == 'qweb-pdf' else 'txt'
            pattern = '/report/excel/'  # if type == 'qweb-pdf' else '/report/text/'
            reportname = url.split(pattern)[1].split('?')[0]

            docids = None
            if '/' in reportname:
                reportname, docids = reportname.split('/')

            if docids:
                # Generic report:
                response = self.report_routes(reportname, docids=docids, converter=converter, context=context)
            else:
                # Particular report:
                data = dict(url_decode(url.split('?')[1]).items())  # decoding the args represented in JSON
                if 'context' in data:
                    context, data_context = json.loads(context or '{}'), json.loads(data.pop('context'))
                    context = json.dumps({**context, **data_context})
                response = self.report_routes(reportname, converter=converter, context=context, **data)

            report = request.env['ir.actions.report'].search([
                ('report_name', '=', reportname)
            ], limit=1)

            if not report:
                return request.not_found()

            if report.excel_out_report_type != 'excel':
                extension = report.excel_out_report_type
            filename = "%s.%s" % (report.name, extension)

            if docids:
                ids = [int(x) for x in docids.split(",")]
                obj = request.env[report.model].browse(ids)
                if report.print_report_name and not len(obj) > 1:
                    eval_context = {
                        'object': obj,
                        'time': __import__('time'),
                        'datetime': __import__('datetime'),
                    }
                    report_name = safe_eval(report.print_report_name, eval_context)
                    filename = "%s.%s" % (report_name, extension)
            response.headers.add('Content-Disposition', content_disposition(filename))
            return response
        res = super(ReportControllerExcel, self).report_download(data, context)
        return res
