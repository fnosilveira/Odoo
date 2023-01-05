
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _product_id_change(self):
        if not self.product_id:
            return
        super()._product_id_change()
        self.name = self.product_id.descr_abrev
