# Copyright (C) 2009  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, fields, models
from odoo.exceptions import UserError


class StockInvoiceOnshipping(models.TransientModel):
    _inherit = "stock.invoice.onshipping"

    def _create_invoice(self, invoice_values):
        
        invoice = super()._create_invoice(invoice_values)
        for invoice_id in invoice:
            for line in invoice_id.invoice_line_ids:
                if line.name != line.product_id.descr_abrev:
                    # deixa a descricao somente com o nome do produto busca_ats
                    line.name = line.product_id.descr_abrev
        return invoice
