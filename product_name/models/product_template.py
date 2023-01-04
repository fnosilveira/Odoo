
from odoo import fields, models

class Products(models.Model):
    
    _inherit = "product.template"
       
    descr_abrev = fields.Text(size=30, required=False, help="Descrição abreviada do produto")
