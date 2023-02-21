# -*- coding: utf-8 -*-

import datetime
from lxml import etree
from odoo import models, fields, api, _
import logging

from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


# class WashType(models.Model):
# 	_name = "em.laundry.mgt.wash.type"

# 	name = fields.Char('Washing Type')
# 	washing_charge = fields.Float('Washing Charge')
# 	responsible_person = fields.Many2one('res.users', string='Responsible Person')
# 	trabajo_externo = fields.Boolean('Trabajo externo')


class OtherThanWash(models.Model):
    _name = "em.laundry.other.than.wash"

    name = fields.Char('Name')
    work_charge = fields.Float('Charge')
    # responsible_person = fields.Many2one('res.users', string='Responsible Person')
    trabajo_externo = fields.Boolean('Trabajo externo')
    comision = fields.Float('Comisión de Servicio')


class Washings(models.Model):
    _name = "em.laundry.mgt.washings"
    _inherit = 'em.laundry.other.than.wash'

    name = fields.Char('Work Name')
    responsible_person = fields.Many2one(
        'res.users', string='Responsible Person')
    date_time = fields.Datetime('Date-Time')
    cloth = fields.Char('Cloth Name')
    cloth_count = fields.Integer('No. Of cloths')
    description = fields.Text('Description')
    order_id = fields.Many2one('sale.order')
    order_line_id = fields.Many2one('sale.order.line')
    washing_states = fields.Selection([
        ('draft', 'Draft'),
        ('assign', 'Assigned'),
        ('process', 'Process'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft', copy=False)
    laundry_track_code = fields.Char('Tracking Code')
    is_make_over = fields.Boolean('Make Over')
    is_make_over_text = fields.Char()
    trabajo_externo = fields.Boolean('Trabajo externo')
    code = fields.Char(string="Code", copy=False)
    date_assign = fields.Date(string="Date Assign", copy=False)
    date_work = fields.Datetime('Fecha/Hora Trabajo')

    @api.model
    def update_washings_status(self):
        washings = self.env['em.laundry.mgt.washings'].browse(
            self.env.context.get('active_ids'))
        washings.write({'washing_states': "done",
                        'date_work': datetime.datetime.now()})
        washings.order_line_id.state_per_washing = 'done'
        
        

    # def comisiones(self):
    # 	self.em_laundry_other_than_wash_comision = self.env['em.laundry.other.than.wash'].search([], limit=1)
    # 	self.comision = self.em_laundry_other_than_wash_comision.comision

    def start_wash(self):
        self.washing_states = 'process'
        # if not self.is_make_over:
        self.responsible_person = self.env.user.id
        self.order_line_id.state_per_washing = 'wash'
        self.date_work = datetime.datetime.now()

    def finish_wash(self):
        self.washing_states = 'done'
        # Verifica se todas a linhas do wash_state estão como done e atualiza o status do pedido no campo all_done
        if self.order_id.washing_count == self.env['em.laundry.mgt.washings'].search_count([('order_id', '=', self.order_id.id), ('washing_states', '=', 'done')]):
            self.order_id.all_done = True
        self.order_line_id.state_per_washing = 'done'


    @api.depends('washing_states')
    def _compute_wash_state(self):
        for rec in self:
            if rec.washing_states == 'done':
                rec.is_done = True
            else:
                rec.is_done = False
        

    def cancel_wash(self):
        self.washing_states = 'cancel'
        self.order_line_id.state_per_washing = 'cancel'


class LaundryTrackTag(models.AbstractModel):
    _name = 'laundry.track.code'

    def _get_report_values(self, docids, data=None):
        return data

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    # def _create_invoice(self, order, so_line, amount):
    #     #Verifica o tipo do faturamento, se for percentual ou valor fixo ele emite um erro ao usuário
    #     if self.advance_payment_method == 'percentage':
    #         raise ValidationError(
    #             'Não é possível faturar um pedido de lavanderia com percentual')
    #     if self.advance_payment_method == 'fixed':
    #         raise ValidationError(
    #             'Não é possível faturar um pedido de lavanderia com valor fixo')

class SaleOrderExtend(models.Model):
    _inherit = "sale.order"

    is_laundry_order = fields.Boolean()
    responsible_person = fields.Many2one('res.users', string='Laundry Person',
                                         default=lambda self: self.env.user)
    state = fields.Selection(
        selection_add=[('draft',), ('order', 'Laundry Order'), ('process', 'Processing'), ('sale',), ('done',),
                       ('complete', 'Completed'), ('return', 'Returned'),
                       ('cancel', 'Cancelled')])
    washing_count = fields.Integer(
        'Ordenes de Trabajo', compute='get_washing_count')
    all_done = fields.Boolean()

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New') and vals.get('is_laundry_order', False):
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['date_order']))
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sale.order.washings.sequence', sequence_date=seq_date) or _('New')
        res = super(SaleOrderExtend, self).create(vals)
        return res

    @api.model
    def _fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(SaleOrderExtend, self)._fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                            submenu=submenu)
        is_laundry_order = self._context.get('default_is_laundry_order', False)

        if is_laundry_order:
            doc = etree.XML(res['arch'])
            nodes = doc.xpath(
                "//page[@name='order_lines']/field[@name='order_line']/tree/field[@name='product_id']")
            for node in nodes:
                node.set('string', "Cloth Name")
                node.set(
                    'domain', "[('type','in',['service','product','consu'])]")
            res['arch'] = etree.tostring(doc)
        return res

    @api.onchange("order_line")
    def enumerar_item(self):
        if self.order_line:
            numero = 1
            for item in self.order_line:
                item.line_number = numero
                item.laundry_track_code = self.name + '-' + str(numero)
                numero += 1

    def _action_cancel(self):
        inv = self.invoice_ids.filtered(lambda inv: inv.state == 'draft')
        inv.button_cancel()
        return self.write({'state': 'cancel'})

    def generate_invoice(self):
        # Call invoice wizard method to create invoice from SO and choose the option to create invoice.

        return {
            'name': _('Create Invoice'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.advance.payment.inv',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_ids': self.ids,
                'active_model': 'sale.order',
                'default_advance_payment_method': 'delivered',
            },
        }

    def action_confirm(self):
        self.enumerar_item()
        if self.is_laundry_order and self.state != 'process':
            self.state = 'order'
        else:
            result = super(SaleOrderExtend, self).action_confirm()
            self.all_done = False
            return result

    def set_to_process(self):
        if self.is_laundry_order:
            for line in self.order_line:
                for other_than in line.other_than_wash_ids:
                    if line.state_per_washing != 'other_than_wash':
                        self.env['em.laundry.mgt.washings'].create({'name': other_than.name,
                                                                    'responsible_person': self.responsible_person.id,
                                                                    'date_time': datetime.datetime.now(),
                                                                    'cloth': line.product_id.name,
                                                                    'cloth_count': line.dress_count_in,
                                                                    'description': line.name,
                                                                    'order_id': line.order_id.id,
                                                                    'order_line_id': line.id,
                                                                    'is_make_over': True,
                                                                    'is_make_over_text': 'Servicios',  # cambios quimer -- Washing
                                                                    'laundry_track_code': line.laundry_track_code,
                                                                    'trabajo_externo': other_than.trabajo_externo,
                                                                    'comision': other_than.comision,

                                                                    })
                if line.product_id.type != 'service':
                    line.state_per_washing = 'done'

                # self.env['em.laundry.mgt.washings'].create({'name': line.wash_type_id.name,
                # 											'responsible_person': line.wash_type_id.responsible_person.id,
                # 											'date_time': datetime.datetime.now(),
                # 											'cloth': line.product_id.name,
                # 											'cloth_count': line.dress_count_in,
                # 											'description': line.name,
                # 											'order_id': line.order_id.id,
                # 											'order_line_id': line.id,
                # 											# 'is_make_over': False,
                # 											'is_make_over_text': 'Washing',
                # 											'laundry_track_code': line.laundry_track_code,
                # 											'trabajo_externo':line.wash_type_id.trabajo_externo
                # 											})
            self.state = 'process'
            for line in self.order_line:
                line.state_per_washing = 'wash'

    def washings_list(self):
        return {
            'name': 'Ordenes de Trabajo',
            'type': 'ir.actions.act_window',
            'res_model': 'em.laundry.mgt.washings',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_id': False,
            'target': 'current',
            'domain': [('order_id', '=', self.id)],
            'context': {'group_by': 'is_make_over_text'}

        }

    def get_washing_count(self):
        for res in self:
            ls = self.env['em.laundry.mgt.washings'].search(
                [('order_id', '=', res.id)]).ids
            res.washing_count = len(ls)
            if res.all_done:
                for line in res.order_line:
                    if line.state_per_washing == 'return':
                        pass
                    else:
                        return
                res.state = 'return'
            else:
                for line in res.order_line:
                    if line.state_per_washing == 'done':
                        pass
                    else:
                        return
                if res.order_line:
                    res.all_done = True

    def return_laundry(self):
        return_lines = []
        for rec in self.order_line:
            return_lines.append([0, 0, {'dress_id': rec.product_id.id,
                                        'qty_in': rec.dress_count_in,
                                        'qty_out': rec.dress_count_out,
                                        'sale_order_line_id': rec.id,
                                        'status': rec.state_per_washing
                                        }])
        res_id = (
            self.env['em.laundry.mgt.laundry.return'].create(
                {'laundry_lines_ids': return_lines})).id
        return {
            'name': 'Returns',
            'type': 'ir.actions.act_window',
            'res_model': 'em.laundry.mgt.laundry.return',
            'view_mode': 'form',
            'view_id': False,
            'res_id': res_id,
            'target': 'new',
        }

    def print_tracking_code(self):
        order_lines = []
        for line in self.order_line:
            extra_work = []
            for extra in line.other_than_wash_ids:
                extra_work.append(extra.name)
            order_lines.append({'cloth_name': line.product_id.name,
                                'quantity_in': line.dress_count_in,
                                'laundry_track_code': line.laundry_track_code,
                                # 'wash_type': line.wash_type_id.name,
                                'other_than_wash': extra_work})

        data = {
            'customer_name': self.partner_id.name,
            'laundry_person': self.responsible_person.name,
            'order_lines': order_lines
        }
        return self.env.ref('rescue.print_tracking_code_tag_action').report_action([],
                                                                                   data={'rec': data})


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    line_number = fields.Integer(string="Item #")
    # wash_type_id = fields.Many2one('em.laundry.mgt.wash.type', string='Wash Type')
    other_than_wash_ids = fields.Many2many(
        'em.laundry.other.than.wash', string='Other Than Wash')
    product_type = fields.Selection(related="product_id.type", store=True)
    dress_count_in = fields.Integer('Quantity In', default=1)
    dress_count_out = fields.Integer('Quantity Out')
    state_per_washing = fields.Selection([
        ('draft', 'Draft'),
        ('wash', 'Servicios'),  # Cambios Quimer --Washing
        # ('other_than_wash', 'Make Over'),
        ('done', 'Done'),
        ('return', 'Returned'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, default='draft')
    laundry_track_code = fields.Char('Tracking Code')

    @api.onchange('product_id')
    def product_id_onchange(self):
        if self.order_id.is_laundry_order:
            wash_type_ids = []
            # self.wash_type_id = None
            self.other_than_wash_ids = None
            self.dress_count_in = 1
            res = {}
            if self.product_id.other_charge_ids and self.product_id.type == 'service':
                wash_type_ids = self.product_id.other_charge_ids.mapped(
                    'other_work_id')
                if wash_type_ids:
                    res = {
                        'domain': {'other_than_wash_ids': [('id', 'in', wash_type_ids.ids)]}
                    }
            return res

    @api.onchange('product_uom_qty', 'other_than_wash_ids', 'dress_count_in')
    def wash_type_id_change(self):
        other_work_charge = 0
        for line in self.filtered(lambda l: l.order_id.is_laundry_order):
            for other_than_wash_id in line.other_than_wash_ids:
                work_charge = sum(oher.price for oher in self.product_id.other_charge_ids.filtered(
                    lambda l: l.other_work_id.id == other_than_wash_id._origin.id))
                if not work_charge:
                    other_work_charge += other_than_wash_id.work_charge
                else:
                    other_work_charge += work_charge
            line.product_uom_qty = line.dress_count_in
            line.price_unit = other_work_charge

    # def get_wash_type_charge(self, wash_type_id, product_id):
    # 	product = self.env['product.product'].browse(product_id)
    # 	for wash_type in product.washing_charge_ids:
    # 		if wash_type.wash_work_id.id == wash_type_id:

    # 			return wash_type.price
    # 	return self.env['em.laundry.mgt.wash.type'].browse(wash_type_id).washing_charge

    def get_other_than_wash_charge(self, other_than_wash_id, product_id):
        product = self.env['product.product'].browse(product_id)
        # for other_charge_id in other_than_wash_ids:
        for other_charge in product.other_charge_ids:
            if other_than_wash_id == other_charge.other_work_id.id:
                return other_charge.price
        return self.env['em.laundry.other.than.wash'].browse(other_than_wash_id).work_charge


class AccountMoveExtended(models.Model):
    _inherit = "account.move"

    is_laundry_invoice = fields.Boolean()


class AccountMoveLineExtend(models.Model):
    _inherit = "account.move.line"

    # wash_type_id = fields.Many2one('em.laundry.mgt.wash.type', string='Wash Type')
    other_than_wash_ids = fields.Many2many(
        'em.laundry.other.than.wash', string='Other Than Wash')

    # def get_wash_type_charge(self, wash_type_id, product_id):
    # 	product = self.env['product.product'].browse(product_id)
    # 	for wash_type in product.washing_charge_ids:
    # 		if wash_type.wash_work_id.id == wash_type_id:

    # 			return wash_type.price
    # 	return self.env['em.laundry.mgt.wash.type'].browse(wash_type_id).washing_charge

    def get_other_than_wash_charge(self, other_than_wash_id, product_id):
        product = self.env['product.product'].browse(product_id)
        for other_charge in product.other_charge_ids:
            if other_than_wash_id == other_charge.other_work_id.id:
                return other_charge.price
        return self.env['em.laundry.other.than.wash'].browse(other_than_wash_id).work_charge


# class ClothWashingCharges(models.Model):
# 	_name = "em.laundry.mgt.washing.charges"

# 	wash_work_id = fields.Many2one('em.laundry.mgt.wash.type', string='Washing')
# 	price = fields.Float('Charges')
# 	product_id = fields.Many2one('product.product')

# 	@api.onchange('wash_work_id')
# 	def wash_work_change(self):
# 		if self.wash_work_id:
# 			self.price = self.wash_work_id.washing_charge


class OtherThanWashingCharges(models.Model):
    _name = "em.laundry.mgt.other.charges"

    other_work_id = fields.Many2one(
        'em.laundry.other.than.wash', string='Other Than Washing')
    price = fields.Float('Charges')
    product_id = fields.Many2one('product.product')

    @api.onchange('other_work_id')
    def other_work_change(self):
        if self.other_work_id:
            self.price = self.other_work_id.work_charge


class ProductProductExtend(models.Model):
    _inherit = "product.product"

    is_wash_type_clothe = fields.Boolean()
    # washing_charge_ids = fields.One2many('em.laundry.mgt.washing.charges', 'product_id')
    other_charge_ids = fields.One2many(
        'em.laundry.mgt.other.charges', 'product_id')
