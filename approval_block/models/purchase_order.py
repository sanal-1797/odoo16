# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseOrder(models.Model):
    """inherit purchase orders and added a new field"""
    _inherit = 'purchase.order'

    approval_block_id = fields.Many2one('approval.block', string='Approval Block', store=True,
                                        compute='_compute_approve_block')

    @api.depends("amount_total")
    def _compute_approve_block(self):
        """The approval block field  filled based on the total amount of PO."""
        for rec in self:
            approval_id = rec.approval_block_id.search([('limit', '<=', rec.amount_total)]).ids

            if not approval_id:
                rec.approval_block_id = False
            else:
                rec.approval_block_id = approval_id[-1]
