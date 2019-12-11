# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit',
                                        default=lambda self:
                                        self.env['res.users'].
                                        operating_unit_default_get(self._uid),
                                        readonly=True,
                                        states={'draft': [('readonly',
                                                           False)]})

    @api.multi
    def finalize_invoice_move_lines(self, move_lines):
        move_lines = super(AccountInvoice,
                           self).finalize_invoice_move_lines(move_lines)
        new_move_lines = []
        for line_tuple in move_lines:
            if self.operating_unit_id:
                line_tuple[2]['operating_unit_id'] = \
                    self.operating_unit_id.id
            new_move_lines.append(line_tuple)
        return new_move_lines

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for pr in self:
            if (
                pr.company_id and
                pr.operating_unit_id and
                pr.company_id != pr.operating_unit_id.company_id
            ):
                raise ValidationError(_('The Company in the Invoice and in '
                                        'Operating Unit must be the same.'))
        return True

    @api.multi
    @api.constrains('operating_unit_id', 'journal_id')
    def _check_journal_operating_unit(self):
        for ai in self:
            if (
                ai.journal_id.operating_unit_id and
                ai.operating_unit_id and
                ai.operating_unit_id != ai.journal_id.operating_unit_id
            ):
                raise ValidationError(_('The OU in the Invoice and in '
                                        'Journal must be the same.'))
        return True


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    operating_unit_id = fields.Many2one('operating.unit',
                                        related='invoice_id.operating_unit_id',
                                        string='Operating Unit', store=True,
                                        readonly=True)
