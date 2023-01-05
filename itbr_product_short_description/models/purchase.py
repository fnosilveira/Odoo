
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _get_product_purchase_description(self, product_lang):
        self.ensure_one()
        name = product_lang.display_name
        if product_lang.short_description:
            name = product_lang.short_description
        return name