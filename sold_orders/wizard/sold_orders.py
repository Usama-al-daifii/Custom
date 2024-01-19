from odoo import models, fields, api, _




class ReprtingSoldOrders(models.TransientModel):
    _name = 'reporting.sold.orders'
    _description = 'Reprting Sold Orders'

    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date to", required=True)
    so_id = fields.Many2one('sale.order')


    def get_report_data(self):
        self = self.sudo()
        domain = []
        date_from = self.date_from
        date_to = self.date_to
        if date_from:
            domain += [('date_order', '>=', date_from)]
        if date_to:
            domain += [('date_order', '<=', date_to)]
        sold_orders = self.env['sale.order'].search(domain, order='date_order asc')
        print('sold_orders > > ', sold_orders)
        all_lines = sold_orders.mapped('order_line')
        all_products = sold_orders.mapped('order_line.product_id')
        # print('all_products', all_products)
        products_qty_list = []
        for product in all_products:
            product_lines = all_lines.filtered(lambda l: l.product_id.id == product.id)
            product_tot_qty = sum(product_lines.mapped('product_uom_qty'))
            products_qty_list.append({'product': product.name, 'product_tot_qty': product_tot_qty})
        products_qty_list.sort(key=lambda i: i['product_tot_qty'], reverse=True)
        top_3_products = products_qty_list[:3]
        # print('top_3_products from base > > ', top_3_products)
        # print('date_from', date_from)
        # print('date_to', date_to)

        return {
            'date_from': date_from,
            'date_to': date_to,
            'sold_orders': sold_orders.ids,
            'top_3_products': top_3_products,

        }

    def get_pdf_report(self):
        data = self.get_report_data()
        print('data > > ', data)
        # sold_orders = data.get('sold_orders', [])
        # top_3_products = data.get('top_3_products', [])
        # print('sold_orders > >', sold_orders)
        # print('top_3_products > >', top_3_products)
        pdf_temp = self.env.ref('sold_orders.action_report_sold_orders_pdf').report_action(self, data=data)
        return pdf_temp

    def get_excel_report(self):
        data = self.get_report_data()
        print('data from get_excel_report > > ', data)
        xlsx_temp = self.env.ref('sold_orders.action_report_sold_orders_xls').report_action(self, data=data)
        return xlsx_temp
