try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None

from io import BytesIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)


class Products(models.Model):
    _inherit = 'product.product'

    qr_code = fields.Char(string="QR Code", tracking=True)
    qr = fields.Binary(string="QR Code File")

    @api.depends('qr_code')
    def generate_qr(self, is_template=False):
        if qrcode and base64:
            if not self.qr_code:
                raise UserError(
                    _('You must enter QR Code number for %s before generating QR Code file.' % self.display_name))
            
            qr = qrcode.QRCode(
                version=4,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.qr_code)
            qr.make(fit=True)

            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            self.write({'qr': qr_image})

        else:
            raise UserError(
                _('Necessary Requirements To Run This Operation Is Not Satisfied'))

    def get_product_by_qr(self, **args):
        return self.env['product.product'].search(
            [('id', '=', self.id), ], limit=1).id

    def write(self, vals):
        res = super(Products, self).write(vals)
        if 'qr_code' in vals and vals['qr_code'] != False:
            self.generate_qr()
        elif 'qr_code' in vals and vals['qr_code'] == False:
            self.write({'qr': False})
        
        return res

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    qr_code = fields.Char(related='product_variant_ids.qr_code',
                          string="QR Code", readonly=False)
    qr = fields.Binary(related='product_variant_ids.qr',
                       string="QR Code File", readonly=False)

    def generate_qr(self):
        product = self.env['product.product'].search(
            [('product_tmpl_id', '=', self.id)])
        for rec in product:
            if rec.qr_code:
                rec.generate_qr(is_template=True)
            else:
                raise UserError(
                    _('You must enter QR Code number for %s before generating QR Code file.' % rec.display_name))
