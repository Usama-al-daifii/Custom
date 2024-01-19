{
    'name': 'Reporting Solds order',
    'version': '1.0.0',
    'category': 'Orders Management',
    'author': 'Usama Aldaifii',
    'summary': 'Reporting Solds order',
    'description': """
    Reporting Solds order to print information about solds order

    """,
    'depends': ['base', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sold_orders_view.xml',
        'report/pdf_report.xml',
        'report/reports.xml'
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
