# -*- coding: utf-8 -*-
from odoo import models, fields, api


class OrderList(models.Model):
    """order list"""
    _name = 'order.list'

    item_name = fields.Char(string='Name')
    description = fields.Char(string='Description')
    quantity = fields.Integer(string='Quantity')
    company_id = fields.Many2one('res.company', copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    unit_price = fields.Monetary(string='Unit price', readonly='True')
    sub_total_price = fields.Monetary(string='Sub Total')

    order_no_id = fields.Many2one('order.food')
    order_item_id = fields.Many2one('order.items')

    @api.onchange('quantity', 'unit_price')
    def _onchange_subtotal(self):
        """Compute subtotal"""
        self.sub_total_price = self.unit_price * self.quantity
