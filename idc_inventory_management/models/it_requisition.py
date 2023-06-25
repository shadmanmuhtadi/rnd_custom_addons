from odoo import api, fields, models
import datetime
class ITRequisition(models.Model):
    _name  = "it.requisition"
    _description = "Product Requisition"
    _rec_name = "employee_id"

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    employee_name = fields.Many2one(string = "Employee Name", comodel_name='res.users',default = lambda self: self.env.user.id)
    department = fields.Many2one(string='Department', related='employee_id.department_id')
    job_title = fields.Char(related='employee_id.job_title', string='Job Position')
    manager = fields.Many2one(related='employee_id.parent_id', string='Manager')
    # designation_id = fields.Many2one(string='Designation', related='employee_id.designation_id')
    doj = fields.Date(string = 'Date of joining')
    work_email = fields.Char(string = 'Work Email')
    work_password = fields.Char(string = 'Work Password')
    erp_id = fields.Char(string = 'ERP ID')
    erp_password = fields.Char(string = 'ERP Password')
    recommendation = fields.Many2many(comodel_name='recommendation.types',string = "Recommendation")
    create_date = fields.Date(string = 'Create Date', default = datetime.datetime.now(), required=True)
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('progress', 'In Progress'),
            ('submitted', 'Submitted'),
            ('cancelled', 'Cancelled'),
        ], default ='draft', string = 'State'
    )

    note = fields.Text(string = 'INTERNAL NOTES')
    def action_draft(self):
        self.state = 'draft'
    def action_confirm(self):
        self.state = 'confirmed'
    def action_progress(self):
        self.state = 'progress'
    def action_submit(self):
        self.state = 'submitted'
    def action_cancel(self):
        self.state = 'cancelled'
class RecommendationTypes(models.Model):
    _name  = "recommendation.types"
    _description = "Recommendation Types"
    _rec_name = "category"

    category = fields.Char(String = 'Category Name', required=True)
    category_responsible = fields.Selection(
        selection=[
            ('it', 'IT'),
            ('admin', 'Admin'),
        ] , string = 'Category Responsible'
    )
