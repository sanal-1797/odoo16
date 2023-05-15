# -*- coding: utf-8 -*-
from odoo import models, fields, _


class SaleOrder(models.Model):
    """inherit and add a button"""
    _inherit = 'sale.order'

    def action_import_order_lines_wizard(self):
        """Button to view Wizard"""

        return {

            'name': _('Import Order Lines Wizard'),
            'type': 'ir.actions.act_window',
            'res_model': 'import.order.lines.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id}
        }
