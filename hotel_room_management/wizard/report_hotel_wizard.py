# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from datetime import datetime, date
from odoo.exceptions import ValidationError
from odoo.tools import date_utils
import io
import json
from odoo.tools.misc import xlsxwriter


class ReportHotelWizard(models.TransientModel):
    """Transient model for wizard"""

    _name = 'report.hotel.wizard'

    partner_id = fields.Many2one('res.partner', string="Guest Name")
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id)

    def fetch_data(self):
        """function to fetch the data """

        query = "SELECT reference_no, res_partner.name , partner_id, check_in , check_out , state FROM accommodation_guest " \
                "INNER JOIN res_partner ON accommodation_guest.partner_id = res_partner.id "

        if self.partner_id and self.date_from and self.date_to:
            """fetching data based on guest,date from and date to"""

            query += f"where partner_id = {self.partner_id.id} AND check_in BETWEEN '{self.date_from}' AND '{self.date_to}'"

        elif self.partner_id and self.date_from:
            """fetching data based on guest and date from"""

            query += f"where partner_id ={self.partner_id.id} AND check_in >= '{self.date_from}'"

        elif self.partner_id and self.date_to:
            """fetching data based on guest and date to"""

            query += f"where partner_id ={self.partner_id.id} AND check_in <= '{self.date_to}'"

        elif self.date_from and self.date_to:
            """"fetching data based on date from and  date to"""

            query += f"where check_in BETWEEN '{self.date_from}' AND '{self.date_to}'"

        elif self.partner_id:
            """fetching data based on guest"""

            query += f"where partner_id = {self.partner_id.id}"
        self.env.cr.execute(query)
        guest = self.env.cr.dictfetchall()

        company_data = {
            "name": self.company_id.name,
            "street": self.company_id.street,
            "city": self.company_id.city,
            "zip": self.company_id.zip,
            "country": self.company_id.country_id.name
        }
        if guest:
            data = {
                    'date_from': self.date_from,
                    'date_to': self.date_to,
                    'partner_name': self.partner_id.name,
                    'guest': guest,
                    'company_data': company_data,
                    'current_date': date.today()
                }
            return data
        else:
            raise ValidationError(_("Nothing To Print"))

    def action_print_report(self):
        """wizard print Button action to print the Report"""

        data = self.fetch_data()
        return self.env.ref('hotel_room_management.action_report_hotel_management').report_action(self, data=data)

    def action_print_xlsx(self):
        """Action to print xlsx report"""

        data = self.fetch_data()
        return {
                'type': 'ir.actions.report',
                'data': {'model': 'report.hotel.wizard',
                         'options': json.dumps(data, default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Excel Report',
                         },
                'report_type': 'xlsx',
            }

    def get_xlsx_report(self, data, response):
        """for get value inside the xlsx report"""

        date_from = data['date_from']
        date_to = data['date_to']
        partner_name = data['partner_name']
        guest = data['guest']
        current_date = data['current_date']

        company_name = data['company_data']['name']
        company_street = data['company_data']['street']
        company_city = data['company_data']['city']
        company_zip = data['company_data']['zip']
        company_country = data['company_data']['country']

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True})
        company_cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'left', 'bold': True})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'left'})
        sheet.set_column(0, 15, 15)

        sheet.merge_range('A8:F9', 'HOTEL MANAGEMENT REPORT', head)

        if date_from:
            sheet.write('A11', 'Date From:', cell_format)
            sheet.write('B11', date_from, txt)
        if date_to:
            sheet.write('A12', 'Date To:', cell_format)
            sheet.write('B12', date_to, txt)
        if partner_name:
            sheet.write('E11', 'Guest name:', cell_format)
            sheet.write('F11', partner_name, txt)

        sheet.write('A2', 'Date:', cell_format)
        sheet.write('B2', current_date, txt)

        sheet.write('A14', 'SI NO', cell_format)
        sheet.write('B14', 'Reference No', cell_format)
        sheet.write('C14', 'Guest', cell_format)
        sheet.write('D14', 'Check-In', cell_format)
        sheet.write('E14', 'Check-Out', cell_format)
        sheet.write('F14', 'State', cell_format)

        sheet.merge_range('D2:E2', company_name, company_cell_format)
        sheet.merge_range('D3:F3', company_street, company_cell_format)
        sheet.write('D4', company_city, company_cell_format)
        sheet.write('E4', company_zip, company_cell_format)
        sheet.write('D5', company_country, company_cell_format)

        col = 15
        si_no = 1
        for rec in guest:
            if rec['state'] == 'draft':
                state = 'Draft'
            if rec['state'] == 'check_in':
                state = 'Check-in'
            if rec['state'] == 'check_out':
                state = 'Check-Out'
            if rec['state'] == 'cancel':
                state = 'Cancel'

            sheet.write(f'A{col}', si_no, txt)
            sheet.write(f'B{col}', rec['reference_no'], txt)
            sheet.write(f'C{col}', rec['name'], txt)
            sheet.write(f'D{col}', rec['check_in'].split()[0], txt)
            if rec['check_out']:
                sheet.write(f'E{col}', rec['check_out'].split()[0], txt)
            sheet.write(f'F{col}', state, txt)

            col += 1
            si_no += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
