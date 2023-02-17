# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class WizardAction(models.TransientModel):
	_name = "wizard.action"

	responsible_person = fields.Many2one('res.users', string='Responsible Person', required=True)
	re_assign_msg = fields.Text(string='Message')
	re_assign = fields.Boolean(string='Reasignar reponsable?')
 
	@api.model
	def default_get(self, fields_list):
		res = super().default_get(fields_list)
		launds = self.env["em.laundry.mgt.washings"].search([
					('id','in',self._context.get('active_ids')), ('washing_states','=','assign')])
		msg = ''
		for l in launds:
			msg += "Esta seguro de cambiar de resposable del lavado con codigo %s " %l.code
		res['re_assign_msg'] = msg if msg != '' else False
		_logger.info('\n\n %r \n\n', res)
		return res

	def aplicar(self):
		state = ['draft']
		if self.re_assign:
			state.append('assign')
		domain = [('id','in',self._context.get('active_ids')),
			('washing_states','in',state)]
		laundry = self.env["em.laundry.mgt.washings"].search(domain)
		if not laundry:
			raise UserError(_("No existing Records"))
		code = self.env['ir.sequence'].next_by_code('washings.sequence')
		data = {
			"responsible_person": self.responsible_person,
			"code": code,
			"washing_states": 'assign',
			"date_assign": fields.Date.context_today(self)
			}
		laundry.write(data)
		action = self.env.ref("rescue.action_window_washing").read()[0]
		action["domain"] = [("id", "in", laundry.ids)]
		return action

class ReporLaundryManagementExternal(models.TransientModel):
	_name = "report.laundry.management.external"

	user_ids = fields.Many2many(comodel_name='res.users', string="Responsibles")
	guide = fields.Selection(selection='_get_selection_guides', string="Guide", required=True)

	@api.model
	def _get_selection_guides(self):
		laundrys = self.env['em.laundry.mgt.washings'].search_read(
			[('washing_states','=','assign')], ['code'], order='code')
		query = """
			SELECT DISTINCT(code) FROM em_laundry_mgt_washings WHERE washing_states = 'assign'
		"""
		self._cr.execute(query)
		res_query = [(r[0],r[0])for r in self._cr.fetchall()]
		_logger.info('\n\n%r \n\n', res_query)
		return res_query

	def print_report_pdf(self):
		return self.env.ref('rescue.action_guia_externa').report_action(self)
		
	
	def _get_datas(self):
		#laundrys = self.env['em.laundry.mgt.washings'].search(
		#	[('responsible_person','in',self.user_ids.ids),('washing_states','=','assign')])
		laundrys = self.env['em.laundry.mgt.washings'].search(
			[('code','=',self.guide)])
		data = {}
		for order in laundrys:
			data.setdefault(order.code, {'data':[]})
			data[order.code].update({
				'responsible': order.responsible_person.name,
				'user': self.env.user.name,
				'guide': order.code,
				'date': order.date_assign
			})
			data[order.code]['data'].append({
				'code': order.laundry_track_code,
				'name': order.name,
			})
		
		result = list(data.values())
		_logger.info('\n\n %r \n\n', result)
		return result