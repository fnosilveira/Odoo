from odoo import models, api
from odoo.http import request


class CustomerBadge(models.AbstractModel):
    _name = 'report.itbrasil_qrcode_print.customer_qr_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data['type'] == 'all':
            dat = [request.env['product.product'].search([('product_tmpl_id', '=', data['data'])])]
        return {
            'data': dat,
        }
