from odoo import models, fields, api

class CustomModule(models.Model):
    _name = 'custom.module'
    _description = 'Custom Module'

    custom_field_1 = fields.Char(string="Custom Field 1")
    custom_field_2 = fields.Integer(string="Custom Field 2")
    model_id = fields.Many2one('ir.model', string="Model")
    field_name = fields.Char(string="Field Name")
    field_type = fields.Selection([
        ('char', 'Char'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('text', 'Text'),
        ('html', 'HTML'),
        ('date', 'Date'),
        ('datetime', 'Datetime'),
        ('binary', 'Binary'),
    ], string='Field Type')
    field_location = fields.Selection([
        ('top', 'Top'),
        ('bottom', 'Bottom'),
        ('inside', 'Inside'),
    ], string='Field Location')

    @api.multi
    def create_custom_fields(self):
        for record in self:
            if record.model_id:
                model = record.model_id
            else:
                model = self.env['ir.model'].search([('model', '=', self._name)])
            model.create({'name': record.field_name, 'field_description': record.field_name, 'ttype': record.field_type})