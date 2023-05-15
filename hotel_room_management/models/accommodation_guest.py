# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta, date
from odoo.exceptions import ValidationError


class AccommodationGuest(models.Model):
    """Accommodation registration"""
    _name = "accommodation.guest"
    _rec_name = "reference_no"
    _inherit = 'mail.thread'
    _description = "accommodation details"

    reference_no = fields.Char(string=' Reference', required=True,
                               default='New', readonly=True, copy=False)

    partner_id = fields.Many2one('res.partner', string='Guest', required=True)

    no_of_guests = fields.Integer(string='No.Of Guest')
    check_in = fields.Datetime(string="Check-In Date and Time", copy=False, default=datetime.today())
    check_out = fields.Date(string="Check-out Date and Time", copy=False)
    bed_type = fields.Selection(string="Bed",
                                selection=[('single', 'Single'), ('double', 'Double'), ('dormitory', 'Dormitory')])
    facilities_ids = fields.Many2many('room.facilities', string="Facilities")

    rooms_id = fields.Many2one('hotel.rooms', string="Rooms", required=True)
    expected_days = fields.Integer(string='Expected Days')
    expected_date = fields.Date(string='Expected Dates')

    guest_details_ids = fields.One2many('guest.details', 'reference_id')
    payment_guest_ids = fields.One2many('payment.guest', 'accommodation_id')
    price_total = fields.Monetary(string='Total', compute='_compute_price_total')
    total_rent = fields.Monetary(string='Total Rent')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    account_id = fields.Many2one('account.move', copy=False, string='Invoice')
    payment_state = fields.Selection(related='account_id.payment_state', copy=False)

    purchase_order_id = fields.Many2one('purchase.order', string="Purchase Order")
    purchase_state = fields.Selection(related='purchase_order_id.state', string='state', store=True)

    state = fields.Selection(
        selection=[
            ('draft', "Draft"),
            ('check_in', "Check-In"),
            ('check_out', "Check-Out"),
            ('cancel', "Cancel")
        ],
        string="Status",
        readonly=True, copy=False,
        default='draft')

    @api.model
    def create(self, vals):
        """for creating accommodation sequence"""
        if vals.get('reference_no', 'New') == 'New':
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'hotel.guest') or 'New'
        return super(AccommodationGuest, self).create(vals)

    # @api.model
    # def purchase_confirm(self):
    #     # do task before confirm
    #     res = super(AccommodationGuest, self).purchase_confirm()
    #     # do task after confirm by using res
    #     return res

    def action_confirm(self):
        """check-in button"""

        # self.purchase_order_id.state = 'sent'
        # self.purchase_order_id.print_quotation()
        self.purchase_order_id.button_confirm()
        # self.action_confirm()

        if self.message_main_attachment_id.id is False:
            raise ValidationError("Please attach document")
        else:

            if self.no_of_guests == 0:
                raise ValidationError("Please provide No.of Guests")
            elif self.no_of_guests > len(self.guest_details_ids):
                raise ValidationError("Please provide all guest details")
            elif self.no_of_guests < len(self.guest_details_ids):
                raise ValidationError("No.of guests and No.of Guest details given are not equal")
            else:
                self.state = 'check_in'
                self.rooms_id.state = 'booked'
                self.rooms_id.room_guest_id = self.partner_id
                self.rooms_id.acc_id = self.id

                self.total_rent = 0
                self.total_rent = self.expected_days * self.rooms_id.rent
                self.payment_guest_ids = [
                    fields.Command.create(
                        {'product_name': 'Room rent', 'product_quantity': self.expected_days,
                         'product_unit_price': self.rooms_id.rent,
                         'product_sub_total_price': self.total_rent})]

    def action_reset_to_draft(self):
        """reset to draft button"""
        # self.purchase_order_id.state = 'draft'
        # if self.purchase_order_id.state == 'sent':
        #     self.purchase_order_id.state = 'draft'
        self.state = 'draft'
        self.rooms_id.state = 'available'

    def action_check_out(self):
        """check out button and invoice creation"""
        self.state = 'check_out'
        self.rooms_id.state = 'available'
        self.check_out = date.today()

        product_lines = []
        for rec in self.payment_guest_ids:
            product_lines.append(fields.Command.create(
                {'name': rec.product_name, 'quantity': rec.product_quantity, 'price_unit': rec.product_unit_price,
                 'price_subtotal': rec.product_sub_total_price}
            ))

        invoice = self.env['account.move'].create([{
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': product_lines,
            'invoice_origin': self.reference_no
        }])
        self.account_id = invoice.id
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'context': self.env.context
        }

    def action_cancel(self):
        """cancel button"""
        self.state = 'cancel'
        self.rooms_id.state = 'available'

    @api.onchange('expected_days')
    def onchange_next_date(self):
        """compute expected date"""
        if self.check_in:
            self.expected_date = date.today() + timedelta(days=self.expected_days)

    @api.depends('payment_guest_ids')
    def _compute_price_total(self):
        """Computing total price"""

        self.price_total = sum(self.payment_guest_ids.mapped('product_sub_total_price'))

    def action_view_invoice(self):
        """view invoice"""

        return {
            'name': "Invoices",
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.account_id.id,
        }

    @api.onchange('facilities_ids', 'bed_type')
    def _onchange_requirements(self):
        """display rooms"""

        room = self.rooms_id.search([('bed', '=', self.bed_type),
                                     ('facilities_ids', '=', self.facilities_ids._origin.ids),
                                     ('state', '=', 'available')]).ids
        return {'domain': {'rooms_id': [('id', 'in', room)]}}

