{
    'name': 'Payroll Customizations',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Custom fields and reports for SunNews Digital Media Channel',
    'description': """
        - Custom fields for Advertiser, RO#, TC No., SPL/PID#, NTN, and GST on Sale Orders and Invoices.
        - Custom Invoice report with Commission column and sign columns.
        - Custom fields for Payslips.
    """,
    'author': 'Aspire Analytica',
    'depends': ['sale', 'account', 'hr_payroll'],
    'data': [
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/hr_payslip_views.xml',
        'reports/invoice_report_templates.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
