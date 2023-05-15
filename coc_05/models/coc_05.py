# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Coc05(models.Model):
    _name = 'coc05'
    _inherit = 'mail.thread'
    _rec_name = 'pass_and_fail'

    pass_and_fail = fields.Selection(string="Resistance", selection=[('Pass', 'Pass'), ('Fail', 'Fail')])
