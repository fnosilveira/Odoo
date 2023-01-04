# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        super().product_id_change()
        vals = {"name": self.product_id.descr_abrev}
        self.update(vals)
