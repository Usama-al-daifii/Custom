from odoo import models


class SoldOrdersXlsx(models.AbstractModel):
    _name = 'report.sold_orders.report_sold_orders_xlsx_temp'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, sold_orders):
        print('data ===========', data)
        # 'sold_orders': [1, 2, 3, 4]
        sold_orders = data.get('sold_orders', [])
        print('sold_orders Before browse===========', sold_orders)
        sold_orders = self.env['sale.order'].sudo().browse(sold_orders)
        top_3_products = data.get('top_3_products', [])
        print('sold_orders after browse===========', sold_orders)
        print('sold_orders ===========', top_3_products)
        format1 = workbook.add_format(
            {
                'align': 'center',
                'font_size': 12,
                'bold': True,
                'border': 2,
                'bg_color': '#00FF00',
            }
        )
        format2 = workbook.add_format(
            {
                'align': 'center',
                'font_size': 12,
                'bold': False,
                'border': 2,
                'bg_color': '#FFFF00'
            }
        )
        date_format = workbook.add_format(
            {
                'align': 'center',
                'font_size': 12,
                'bold': False,
                'border': 2,
                'bg_color': '#FFFF00',
                'num_format': 'mmm d yyyy hh:mm AM/PM'
            }
        )
        sheet = workbook.add_worksheet('Sold Orders')
        sheet.set_column(0, 2, 30)

        # sheet.set_column('A', 15)
        # sheet.set_column('B', 10)
        sheet.write('A1', 'Sold Order Period :', format1)
        sheet.write('A2', 'Date From :', format1)

        sheet.write('B2', data.get('date_from', ''), format2)
        sheet.write('A3', 'Date To :', format1)

        sheet.write('B3', data.get('date_to', ''), format2)
        sheet.write('A5', 'Sold Order Information : ', format1)
        sheet.write('A6', 'Order Number', format1)
        sheet.write('B6', 'Customer', format1)
        sheet.write('C6', 'Order Date', format1)
        row = 6
        col = 0
        sheet.write('A' + str(row + len(sold_orders) + 2), 'Top 3 Products', format1)
        sheet.write('A' + str(row + len(sold_orders) + 3), 'Product', format1)
        sheet.write('B' + str(row + len(sold_orders) + 3), 'Quantity', format1)
        print('top_3_products[0]------>', top_3_products[0].get('product'))
        sheet.write('A' + str(row + len(sold_orders) + 4), top_3_products[0].get('product'), format2)
        sheet.write('B' + str(row + len(sold_orders) + 4), top_3_products[0].get('product_tot_qty'), format2)
        sheet.write('A' + str(row + len(sold_orders) + 5), top_3_products[1].get('product'), format2)
        sheet.write('B' + str(row + len(sold_orders) + 5), top_3_products[1].get('product_tot_qty'), format2)
        sheet.write('A' + str(row + len(sold_orders) + 6), top_3_products[2].get('product'), format2)
        sheet.write('B' + str(row + len(sold_orders) + 6), top_3_products[2].get('product_tot_qty'), format2)

        for so in sold_orders:
            sheet.write('A' + str(row + 1), so.name, format2)
            print('so.date_order --> ', so.date_order)
            sheet.write('B' + str(row + 1), so.partner_id.name, format2)
            sheet.write('C' + str(row + 1), so.date_order, date_format)
            row += 1
        # print('row   ----->  ', row)
        # sheet.write('A' + str(row + len(sold_orders)), 'Top 3 Products', format1)
        # sheet.write('A' + str(row + len(sold_orders)), 'Product', format1)
        # sheet.write('B' + str(row + len(sold_orders)), 'Quantity', format1)
        # print('row after Top    ----->  ', row)
        # for prod in top_3_products:
        #     sheet.write('A' + str(row + len(sold_orders) + 1), prod.get('product'), format2)
        #     sheet.write('B' + str(row + len(sold_orders) + 1), prod.get('product_tot_qty'), format2)
