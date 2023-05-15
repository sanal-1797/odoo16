# -*- coding: utf-8 -*-

from odoo import models, api


class HotelReport(models.AbstractModel):
    """Abstract model for Hotel report"""
    _name = 'report.hotel_room_management.report_hotel'

    @api.model
    def _get_report_values(self, docids, data=None):
        """to print report"""

        return {
            'doc_ids': docids,
            'doc_model': 'accommodation.guest',
            'data': data,

        }
