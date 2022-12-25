
{
    'name': 'Product QR Code',
    'version': '14.0..0.1',
    'summary': 'Print QR Code for Product',
    'description': 'QR Code, QR Code Generator, Odoo QR Code Generator, Print QR Code',
    'category': 'Extra Tools',
    'author': 'IT Brasil',
    'maintainer': 'IT Brasil',
    'company': 'IT Brasil',
    'website': 'https://www.itbrasil.com.br',
    'depends': ['base', 'sale', 'stock'],
    'data': [
        'report/paperformat.xml',
        'report/report.xml',
        'views/view.xml',
        'report/template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
