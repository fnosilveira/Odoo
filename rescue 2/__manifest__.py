# -*- coding: utf-8 -*-
{
    'name': "Servicios",
    'summary': """Put on wings to your Laundry Business""",
    'description': """
        This app will manage the laundry and their works, And Put on wings to your Laundry Business.
    """,
    'author': 'ErpMstar Solutions',
    'category': 'LimaFac/Sales',
    'version': '1.0',
    'depends': ['sale'],
    # always loaded
    'data': [
        'data/sequence.xml',
        'data/estado.xml',
        'security/rescue_group.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'wizards/return_wizard.xml',
        'wizards/wizard.xml',
        'wizards/wizard_action.xml',
        'reports/laundry_report.xml',
        'reports/tracking_code_tag.xml',
        'reports/receipt_ticket_venta.xml',
        'reports/guia_externa.xml',
        'views/menuitem_laundry.xml',
    ],
    'images': [
        'static/description/main.jpg',
    ],
    'installable': True,
    'website': '',
    'auto_install': False,
    'price': 70,
    'currency': 'USD',
}
