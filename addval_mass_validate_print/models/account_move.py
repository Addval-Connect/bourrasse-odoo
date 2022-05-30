# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
from odoo import fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_mass_validate(self):
        return {
            'name': _('Bulk Validate'),
            'res_model': 'validate.account.move',
            'view_mode': 'form',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'active_model': 'account.move',
                'active_ids': self.ids,
            },
        }

    def action_mass_print(self):
        attachment_ids = []
        for rec in self:
            report = self.env.ref('account.account_invoices')._render_qweb_pdf(rec.ids)
            filename = f"{rec.l10n_latam_document_number}_{rec.partner_id.name_get()[0][1]}.pdf"
            invoice_pdfs = self.env['ir.attachment'].create({
                'name': filename,
                'type': 'binary',
                'datas': base64.b64encode(report[0]),
                'res_model': 'account.move',
                'res_id': rec.id,
                'mimetype': 'application/pdf'
            })
            attachment_ids.append(invoice_pdfs.id)
        return {
            'type': 'ir.actions.act_url',
            'url': '/print/invoices?attachment_ids=%(attachment_ids)s' % {'attachment_ids': ','.join(str(x) for x in attachment_ids)},
        }


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    # Default set 'Credit Notes' journal
    def default_get(self, fields):
        res = super(AccountMoveReversal, self).default_get(fields)
        if self._context.get('is_from_credit_note'):
            res['journal_id'] = self.env.ref('addval_mass_validate_print.credit_note_journal').id
        return res


class ValidateAccountMove(models.TransientModel):
    _inherit = "validate.account.move"

    # Validation: Bulk validate is apply only on unpaid invoices.
    def validate_move(self):
        selected_ids = self._context.get('active_ids')
        AccountMoves = self.env['account.move'].browse(selected_ids).filtered(lambda x: x.payment_state == 'not_paid')
        if AccountMoves:
            invoice_numbers = [rec + '\n' for rec in AccountMoves.mapped('name')]
            raise UserError(_("Please remove below Invoices. \n%s" % ''.join(invoice_numbers)))
        return super(ValidateAccountMove, self).validate_move()