# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.onchange("product_id")
    def _onchange_product_id_fiscal(self):
        super()._onchange_product_id_fiscal()
        if self.product_id:
            self.name = self.product_id.descr_abrev
