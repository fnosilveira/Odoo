# Copyright (C) 2022 - TODAY Filipe Silveira - IT Brasil
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


## Cria um botão para enviar mensagem no pedido de venda via WhatsApp utilizando o Twilio

from odoo import models, fields, api
from twilio.rest import Client
import logging



class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    
    def send_whatsapp(self):

        
        account_sid = self.company_id.whatsapp_twillio_SID
        auth_token = self.company_id.whatsapp_twillio_token
        client = Client(account_sid, auth_token)
        url = self.get_pdf_link()
        url = url.replace('http://', 'https://')

        
        logging.warning(url)
        message = client.messages.create(
            body='Olá, ' + self.partner_id.name + ' seu pedido foi enviado com sucesso!',
            from_='whatsapp:' + self.company_id.whatsapp_twillio_phone.replace(' ', '').replace('-',''),
            to='whatsapp:' + self.partner_id.mobile.replace(' ', '').replace('-',''),
            ## SEND A LOCAL PDF ATTACHMENT TO THE CUSTOMER
            media_url=[url]
            
        )
        logging
        logging.info(message.sid)
        return True

    def get_pdf_link(self):
        url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url += '/report/pdf/sale.report_saleorder/' + str(self.id) 
        return url
        




    
            


    
    