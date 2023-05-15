# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class Sales(http.Controller):
    @http.route(['/top_customers'], type="json", auth="public")
    def top_customers(self):
        """to find the top 10 customers"""

        website_ids = request.env['website'].sudo().search([]).ids
        sale_obj = request.env['sale.order'].sudo().search([
            ('state', 'in', ['done', 'sale']),
            ('website_id', 'in', website_ids),
        ])

        partners_ids = [sale_order.partner_id for sale_order in sale_obj]

        most_sale_partner = []
        for rec in partners_ids:
            most_sale_partner.append({'partner': rec,
                                      'count': partners_ids.count(rec)})

        most_sale_partner = sorted(most_sale_partner, key=lambda x: x['count'], reverse=True)

        unique_customers_list = []
        for i in range(len(most_sale_partner)):
            if most_sale_partner[i] not in most_sale_partner[i + 1:]:
                unique_customers_list.append(most_sale_partner[i])

        customers = []
        for record in unique_customers_list:
            customers.append({'partner_name': record['partner'].name, 'partner_id': record['partner'].id,
                              'order_count': record['count']})
        customers = customers[:10]
        return customers

    @http.route('/partner/<model("res.partner"):partner>', type='http', auth="user", website=True)
    def product_details(self, partner):
        values = {
            'partner': partner,
        }
        return request.render('top_10_customers.customer_details', values)


