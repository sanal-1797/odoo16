# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class MaterialRequest(models.Model):
    """Model for material request"""

    _name = 'material.request'
    _rec_name = "request_no"
    _description = "Material Request"
    _inherit = 'mail.thread'

    request_no = fields.Char(string='Request NO.', default='New', required=True, readonly=True)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    product_line_ids = fields.One2many('product.lines', 'connect_material_request_id')
    purchase_order_ids = fields.Many2many('purchase.order', string='Purchase orders')
    internal_transfer_ids = fields.Many2many('stock.picking', string='Internal transfer')
    date_field = fields.Datetime(string='Date & Time', default=datetime.today())
    purchase_count = fields.Integer(string='Purchase Count')
    internal_transfer_count = fields.Integer(string='Internal Transfer Count')

    state = fields.Selection(
        selection=[
            ('draft', "Draft"),
            ('request', "Request pending"),
            ('manager_approved', "Manager Approved"),
            ('head_approved', "Head Approved"),
            ('reject', "Reject")
        ],
        string="Status",
        readonly=True, copy=False,
        default='draft')

    @api.model
    def create(self, vals):
        """sequence for Material request"""

        if vals.get('request_no', 'New') == 'New':
            vals['request_no'] = self.env['ir.sequence'].next_by_code(
                'material.request.sequence') or 'New'
            return super().create(vals)

    def action_request(self):
        """Request button and also merge the order lines"""

        if self.product_line_ids:
            for rec in self.product_line_ids:
                if rec.id in self.product_line_ids.ids:
                    line_ids = self.product_line_ids.filtered(
                        lambda
                            m: m.product_id.id == rec.product_id.id and m.operations == rec.operations and m.destination_location == rec.destination_location)
                    print(line_ids)
                    quantity = 0
                    for qty in line_ids:
                        quantity += qty.pro_qty

                    if quantity >= 1:
                        line_ids[0].write({'pro_qty': quantity,
                                           'connect_material_request_id': line_ids[0].connect_material_request_id.id})
                        line_ids[1:].unlink()
            self.state = 'request'

        else:
            raise ValidationError("Add at least one product ")

    def action_manger_approve(self):
        """Button for to get approve from manager"""

        self.state = 'manager_approved'

    def action_head_approve(self):
        """Approved button for creating purchase orders or internal transfer"""

        # generate purchase orders
        for rec in self.product_line_ids:
            if rec.operations == 'rfq':
                for rec_vendor in rec.product_id.seller_ids:
                    purchase_order = self.env['purchase.order'].create([{'partner_id': rec_vendor.partner_id.id,
                                                                         'order_line': [fields.Command.create(
                                                                             {'product_id': rec.product_id.id,
                                                                              'product_qty': rec.pro_qty,
                                                                              'price_unit': rec_vendor.price
                                                                              }
                                                                         )]
                                                                         }])
                    self.purchase_order_ids = [fields.Command.link(purchase_order.id)]
                self.purchase_count = len(self.purchase_order_ids.ids)

        # generate internal transfers
        internal_filtered_list = []
        for record in self.product_line_ids:
            if record.operations == 'internal_transfer':

                if record.id in self.product_line_ids.ids:
                    internal_ids = self.product_line_ids.filtered(
                        lambda value: value.destination_location.id == record.destination_location.id)
                internal_filtered_list.append(internal_ids)

        internal_set = set(internal_filtered_list)

        for rec_intern in internal_set:
            print(rec_intern.ids)
            internal_list = []
            for rec_int_transfer in rec_intern:
                internal_list.append(fields.Command.create({
                    'product_id': rec_int_transfer.product_id.id,
                    'product_uom_qty': rec_int_transfer.pro_qty,
                    'location_id': rec_int_transfer.source_location.id,
                    'location_dest_id': rec_int_transfer.destination_location.id,
                    'name': 'Internal Transfer'
                }))

            transfer_order = self.env['stock.picking'].create(
                [{'location_id': rec_int_transfer[0].source_location.id,
                  'location_dest_id': rec_int_transfer[0].destination_location.id,
                  'picking_type_id': self.env['stock.picking.type'].search([('code', '=', 'internal')]).id,
                  'move_ids': internal_list
                  }])

            self.internal_transfer_ids = [fields.Command.link(transfer_order.id)]

        self.internal_transfer_count = len(self.internal_transfer_ids)

        self.state = 'head_approved'

    def action_reject(self):
        """Reject button"""

        self.state = 'reject'

    def action_view_purchase_orders_list(self):
        """smart tab to view purchase order list"""

        purchase_ids = self.purchase_order_ids.ids
        return {
            'name': "Purchases",
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', purchase_ids)],
            'context': {'create': False}
        }

    def action_view_internal_transfers_list(self):
        """smart tab to view internal transfers list"""

        internal_ids = self.internal_transfer_ids.ids
        return {
            'name': "Internal Transfer",
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', internal_ids)],
            'context': {'create': False}
        }
