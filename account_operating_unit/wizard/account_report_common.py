# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountCommonReport(models.TransientModel):
    _inherit = "account.common.report"

    operating_unit_ids = fields.Many2many('operating.unit',
                                          string='Operating Units',
                                          required=False)

    def _build_contexts(self, data):
        result = super(AccountCommonReport, self)._build_contexts(data)
        data2 = {}
        data2['form'] = self.read(['operating_unit_ids'])[0]
        result['operating_unit_ids'] = \
            'operating_unit_ids' in data2['form'] \
            and data2['form']['operating_unit_ids'] or False
        return result
