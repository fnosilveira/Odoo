
from odoo import _,fields, models, api
from odoo.exceptions import UserError, ValidationError 

class Products(models.Model):

    _inherit = "product.template"

    descr_abrev = fields.Char(help="Descrição abreviada do produto", required=True, size=120) 
