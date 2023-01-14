{
    'name': 'Create Custom Fields',
    'version': '14.1.0.0',
    'summary': 'Create custom fields for any model',
    'description': 'Create custom fields for any model',
    'category': 'Extra Tools',
    'author': "Filipe Silveira, IT Brasil",
    'maintainer': ['it-brasil', 'fnosilveira'],
    'company': 'IT Brasil',
    'website': 'https://itbrasil.com.br',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/custom_fields_view.xml',

    ],
    'installable': True,
    'application': True ,
    'auto_install': False,
}
