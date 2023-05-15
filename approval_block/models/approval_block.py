# -*- coding: utf-8 -*-
from odoo import models, fields


class ApprovalBlock(models.Model):
    _name = 'approval.block'
    _description = 'Approval Block'
    _inherit = 'mail.thread'

    name = fields.Char(string='Name')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    limit = fields.Monetary(string='Limit')
