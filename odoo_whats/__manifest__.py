# Copyright (C) 2022 - TODAY Filipe Silveira - IT Brasil
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Odoo Whats",
    "summary": "Conecta o Odoo com o WhatsApp utilizando API da Twilio",
    "category": "API",
    "license": "AGPL-3",
    "author": "Filipe Silveira",
    "maintainers": ["fnosilveira", "it-brasil"],
    "version": "16.0.0.1",
    "depends": ["base", "mail", "contacts", "sale", "purchase", "account"],
    "data": [
        'views/res_company.xml',
        'views/sale_order.xml',
    ],
    "demo": [],
    "installable": True,
}
