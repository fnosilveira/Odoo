# Copyright (C) 2022 - TODAY Filipe Silveira - IT Brasil
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


## Cria os campos para TOKEN e Número de telefone na configuração da empresa

from odoo import models, fields, api

class ResCompany(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'

    whatsapp_twillio_token = fields.Char(string='Twilio Token')
    whatsapp_twillio_phone = fields.Char(string='Twilio Phone')
    whatsapp_twillio_account = fields.Char(string='Twilio Account')
    whatsapp_twillio_SID = fields.Char(string='Twilio SID')


    