# -*- coding: utf-8 -*-
from odoo import models, fields


class OrderCategory(models.Model):
    """for creating order category"""
    _name = 'order.category'
    _rec_name = 'order_category'

    order_category = fields.Char(string='Category')
