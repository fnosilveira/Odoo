
{
    'name': 'Product QR Code',
    'version': '14.2.0.0',
    'summary': 'Print QR Code for Product',
    'description': 'QR Code, QR Code Generator, Odoo QR Code Generator, Print QR Code',
    'category': 'Extra Tools',
    'author': "Filipe Silveira, IT Brasil",
    'maintainer': ['it-brasil', 'fnosilveira'],
    'company': 'IT Brasil',
    'website': 'https://itbrasil.com.br',
    'depends': ['product'],
    'data': [
        'report/paperformat.xml',
        'report/product_reports.xml',
        'views/product_views.xml',
        'report/template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
