try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None
from io import BytesIO
import logging

from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError


class Products(models.Model):
    _inherit = 'product.template'

    qr_code = fields.Char(string="QR Code")
    qr = fields.Binary(string="QR Code")

    @api.depends('qr_code')
    def generate_qr(self):
        logging.warning("GERANDO QR %s", self.qr_code)
        if self.qr_code == False:
            raise UserError(_('Não foi possivel gerar o QR Code. Verifique se o produto contám o campo QR Code preenchido.'))
        else:
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
            logging.info("QRIMAGE %s", qr_image)
            self.qr = qr_image
            product = self.env['product.template'].search(
                [('qr_code', '=', self.id)])
            logging.info("PRODUTO %s", product)
            for rec in product:
                rec.generate_qr()
            return self.env.ref('itbrasil_qrcode_print.print_qr2').report_action(
                self, data={'data': self.id, 'type': 'all'})

       
    
    def get_product_by_qr(self, **args):
        return self.env['product.template'].search(
            [('sequence', '=', self.id), ], limit=1).id



