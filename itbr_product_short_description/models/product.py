# Copyright 2023 IT Brasil  (https://itbrasil.com.br)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    short_description = fields.Char(
        help="Short product description",
        size=120,
        translate=True,
    )


class ProductTemplate(models.Model):
    _inherit = "product.template"

    short_description = fields.Char(
        related="product_variant_ids.short_description", readonly=False
    )
