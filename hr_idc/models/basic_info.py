from odoo import api, fields, models

class PersonalInfo(models.Model):
    _inherit = "hr.employee"

    personal_email = fields.Char(string='Personal Email', Tracking=True)
    personal_contact = fields.Char(string='Personal Mobile', Tracking=True)

    present_add = fields.Char(string='Present Address')
    permanent_add = fields.Char(String="Permanent Address")
    employee_id = fields.Char(string='Employee ID')

    emergency_contact_name = fields.Char(string='Contact Person Name')
    emergency_contact_address = fields.Char(string='Contact Person Address')
    emergency_contact_relation_id = fields.Many2one('hr.employee.relation', string='Contact Person Address')
    recruitment_type = fields.Selection([
        ('new', 'New'),
        ('replacement', 'Replacement'),
        ('rejoin', 'Rejoin')], string='Recruitment Type')
    post_code_id = fields.Many2one('hr.employee.postcode', string='Post Code')


    present_house = fields.Char()
    present_area = fields.Char()
    present_zip = fields.Char(change_default=True)
    present_Thana = fields.Char()
    present_district = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    present_division = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    present_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')

    permanent_house = fields.Char()
    permanent_area = fields.Char()
    permanent_zip = fields.Char(change_default=True)
    permanent_Thana = fields.Char()
    permanent_district = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    permanent_division = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    permanent_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')


    # @api.model
    # def create(self, vals):
    #     vals['employee_id'] = self.env['ir.sequence'].next_by_code('employee.id')
    #     return super(PersonalInfo, self).create(vals)
    
    # def write(self, vals):
    #     if not self.employee_id and not vals.get('employee_id'): #when there is no value in ref and no newly written value in ref
    #         vals['employee_id'] = self.env['ir.sequence'].next_by_code('employee.id')
    #     return super(PersonalInfo, self).write(vals)

class PostCode(models.Model):
    _name = 'hr.employee.postcode'
    _rec_name = 'post_code'
    post_code = fields.Char(string="Post Code")