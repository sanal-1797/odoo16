# -*- coding: utf-8 -*-
from odoo import models, fields


class EmployeeTransfer(models.Model):
    """Transfer employee from one company to another company"""
    _name = "employee.transfer"
    _rec_name = "employee_id"
    _description = "Employee Transfer"
    _inherit = 'mail.thread'

    employee_id = fields.Many2one('hr.employee')
    current_company_id = fields.Many2one(related='employee_id.company_id', string='Current Company')
    new_company_id = fields.Many2one('res.company', string='New Company')
    state = fields.Selection(
        selection=[
            ('draft', "Draft"),
            ('request', "Request pending"),
            ('approved', "Approved"),
            ('cancel', "Cancel")
        ],
        string="Status",
        readonly=True, copy=False,
        default='draft')

    def action_request(self):
        """request for transfer"""
        self.state = 'request'

    def action_approve(self):
        """approved button to transfer employee to another company"""

        # copying current employee
        new_employee = self.employee_id.copy({'company_id': self.new_company_id.id})
        new_employee.name = new_employee.name.strip('(copy)')
        self.employee_id.active = False
        self.employee_id = new_employee.id

        # state changes to approved
        self.state = 'approved'

        return new_employee

    def action_cancel(self):
        """Cancel button"""

        self.state = 'cancel'
