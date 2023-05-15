# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductLines(models.Model):
    """Model for product lines"""
    _name = 'product.lines'

    connect_material_request_id = fields.Many2one('material.request', string="Connect", readonly=True)
    product_id = fields.Many2one('product.product', string="Product")
    operations = fields.Selection(
        selection=[
            ('rfq', "RFQ"),
            ('internal_transfer', "Internal Transfer")
        ],
        string="Operations",
        copy=False,
        default='rfq',
        required='1')
    pro_qty = fields.Integer(string='Quantity', default=1)
    source_location = fields.Many2one('stock.location', string='Source Location')
    destination_location = fields.Many2one('stock.location', string='Destination Location')

    @api.onchange('operations')
    def _onchange_operations(self):
        """if operation is internal transfer,then default source location will be wh/stock"""

        if self.operations == 'internal_transfer':
            self.source_location = self.env.ref('stock.stock_location_stock').id
        else:
            self.source_location = False
