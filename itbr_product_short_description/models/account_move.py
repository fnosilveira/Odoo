# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_computed_name(self):
        self.ensure_one()
        if self.product_id:
            product = self.product_id.with_context(
                lang=self.partner_id.lang)
            if product.short_description:
                return product.short_description
        return super(AccountMoveLine, self)._get_computed_name()