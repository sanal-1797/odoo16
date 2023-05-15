# -*- coding: utf-8 -*-
from odoo import models, fields, api


class OrderItems(models.Model):
    """item order management"""
    _name = 'order.items'
    _rec_name = 'item_name'

    item_name = fields.Char(string='Product Name')
    item_category = fields.Many2many('order.category', string='Category')
    company_id = fields.Many2one('res.company', copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    item_price = fields.Monetary(string="Price")
    item_image = fields.Image(string='image')

    order_no_id = fields.Many2one('order.food')
    order_quantity = fields.Integer(string="Quantity")
    order_sub_total = fields.Monetary(string='subtotal', compute='_compute_subtotal')

    @api.depends('order_quantity', 'item_price')
    def _compute_subtotal(self):
        self.order_sub_total = self.order_quantity * self.item_price

    def add_to_list(self):
        """add to list and add the list to payment page in accommodation"""
        self.order_no_id.order_list_ids = [
            fields.Command.create(
                {'item_name': self.item_name, 'quantity': self.order_quantity, 'unit_price': self.item_price,
                 'sub_total_price': self.order_sub_total})]

        self.order_no_id.order_room.acc_id.payment_guest_ids = [
            fields.Command.create(
                {'product_name': self.item_name, 'product_quantity': self.order_quantity,
                 'product_unit_price': self.item_price,
                 'product_sub_total_price': self.order_sub_total})]

        self.order_quantity = 1

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'order.food',
            'res_id': self.order_no_id.id,
            'context': self.env.context
        }
