# -*- coding: utf-8 -*-
from odoo import models, fields


class PaymentGuest(models.Model):
    """payment guest"""
    _name = 'payment.guest'

    product_name = fields.Char(string='Name')
    product_description = fields.Char(string='Description')
    product_quantity = fields.Integer(string='Quantity')
    product_uom = fields.Many2one('uom.uom',string='UOM')
    company_id = fields.Many2one('res.company', copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    product_unit_price = fields.Monetary(string='Unit price', readonly='True')

    product_sub_total_price = fields.Monetary(string='Sub Total')

    accommodation_id = fields.Many2one('accommodation.guest')
