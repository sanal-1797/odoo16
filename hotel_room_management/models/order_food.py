# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime


class OrderFood(models.Model):
    """for ordering food"""
    _name = 'order.food'
    _rec_name = 'order_no'
    _inherit = 'mail.thread'
    _description = 'Order'

    order_no = fields.Char(string="Order NO.", default='New', required=True, readonly=True)
    order_room = fields.Many2one('hotel.rooms', string="Room")
    guest_name = fields.Many2one(string="Guest Name", related='order_room.room_guest_id')
    order_date = fields.Datetime(string="Order Date", copy=False, default=datetime.today())
    category_ids = fields.Many2many('order.category', string='Category')

    order_items_ids = fields.One2many('order.items', 'order_no_id')
    order_list_ids = fields.One2many('order.list', 'order_no_id')

    company_id = fields.Many2one('res.company', copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    price_total = fields.Monetary(string='Total', compute='_compute_price_total')

    @api.model
    def create(self, vals):
        """for creating order sequence"""
        if vals.get('order_no', 'New') == 'New':
            vals['order_no'] = self.env['ir.sequence'].next_by_code(
                'order.sequence') or 'New'
        return super().create(vals)

    @api.onchange('category_ids')
    def onchange_category_ids(self):
        """for adding items in Menu"""
        self.order_items_ids = False

        rec = self.env['order.items'].search([('item_category', 'in', self.category_ids.ids)])
        self.write({'order_items_ids': rec.ids})

    @api.depends('order_list_ids')
    def _compute_price_total(self):
        """Computing total price"""

        self.price_total = sum(self.order_list_ids.mapped('sub_total_price'))


