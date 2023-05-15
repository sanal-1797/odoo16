# -*- coding: utf-8 -*-

from odoo import models, fields


class Coc(models.Model):
    """Clash of codes"""

    _name = 'coc'
    _inherit = 'mail.thread'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', string='Partner')
