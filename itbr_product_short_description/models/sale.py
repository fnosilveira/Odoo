# Copyright 2023 IT Brasil  (https://itbrasil.com.br)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        if self.product_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang)
            if product.short_description:
                self.name = product.short_description
        return res
