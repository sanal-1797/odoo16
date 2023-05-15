# -*- coding: utf-8 -*-
from odoo import models, fields
import openpyxl
import base64
from io import BytesIO


class ImportOrderLinesWizard(models.TransientModel):
    """Transient model for wizard"""
    _name = 'import.order.lines.wizard'

    file = fields.Binary(string="File", required=True)
    file_name = fields.Char(string="File name")
    order_id = fields.Many2one('sale.order')

    def action_import_order_lines(self):
        """Button to import order lines from xls sheet"""
        wb = openpyxl.load_workbook(filename=BytesIO(base64.b64decode(self.file)), read_only=True)
        ws = wb.active

        for record in ws.iter_rows(min_row=2, max_row=None, min_col=None, max_col=None, values_only=True):
            search_product = self.env['product.product'].search([('name', '=', record[0])])
            if search_product:
                self.order_id.order_line = [fields.Command.create({'product_id': search_product.id,
                                                                   'name': record[3] or search_product.name,
                                                                   'product_uom_qty': record[1] or 1,
                                                                   'price_unit': record[4] or search_product.lst_price,
                                                                   'product_uom': search_product.uom_id.id})]

            if not search_product:
                new_product = self.env['product.product'].create({
                    'name': record[0],
                    'uom_id': self.env['uom.uom'].search(
                        [('name', '=', record[2])]).id,
                    'uom_po_id': self.env['uom.uom'].search(
                        [('name', '=', record[2])]).id,
                    'lst_price': record[4]
                })

                self.order_id.order_line = [fields.Command.create({'product_id': new_product.id,
                                                                   'name': record[3],
                                                                   'product_uom_qty': record[1],
                                                                   'price_unit': record[4],
                                                                   'product_uom': new_product.uom_id.id})]
