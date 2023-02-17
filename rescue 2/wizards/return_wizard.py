# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class LaundryReturn(models.TransientModel):
    _name = "em.laundry.mgt.laundry.return"

    laundry_lines_ids = fields.One2many('em.laundry.mgt.laundry.return.line', 'laundry_return_id')

    def set_return(self):
        order_line_id = None
        for laundry_line in self.laundry_lines_ids:
            order_line_id = self.env['sale.order.line'].browse(laundry_line.sale_order_line_id.id)
            if order_line_id.dress_count_in < laundry_line.qty_out:
                raise UserError('Can not return more than taken')
            if laundry_line.qty_out < 0:
                raise UserError('Can not return negative')
            order_line_id.dress_count_out = laundry_line.qty_out
            order_line_id.state_per_washing = laundry_line.status
        order_line_id.order_id.get_washing_count()


class LaundryReturnLine(models.TransientModel):
    _name = "em.laundry.mgt.laundry.return.line"

    dress_id = fields.Many2one('product.product')
    qty_in = fields.Integer('Quantity In')
    qty_out = fields.Integer('Quantity Out')
    status = fields.Selection([('done', 'Done'), ('return', 'Return')], default='done')
    laundry_return_id = fields.Many2one('em.laundry.mgt.laundry.return')
    sale_order_line_id = fields.Many2one('sale.order.id')
