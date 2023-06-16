from odoo import api, fields, models
from datetime import date
import datetime

class PersonalInfo(models.Model):
    _inherit = "hr.employee"

    religion = fields.Selection([
        ('islam', 'Islam'),
        ('hindu', 'Hindu'),
        ('christian', 'Christian')],tracking=True)
    t_shirt_size = fields.Selection([
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL')],string='T-Shirt Size',tracking=True)
    blood_grp = fields.Selection([
        ('a_pos', 'A+'),
        ('a_neg', 'A-'),
        ('b_pos', 'B+'),
        ('b_neg', 'B-'),
        ('ab_pos', 'AB+'),
        ('ab_neg', 'AB-'),
        ('O_pos', 'O+'),
        ('o_neg', 'O-')],string='Blood Group',tracking=True)
    nid_no = fields.Char(string='NID')
    tin_no = fields.Char(string='TIN No')

    academic_ids = fields.One2many(
        'hr.employee.academic', 'employee_id',
        string='Academic', help='Academic Information')

    previous_employment_history_ids = fields.One2many(
        'hr.employee.previous.employment.history', 'employee_id',
        string='Previous Employment History', help='Previous Employment Information')
    employment_summery_ids = fields.One2many(
        'hr.employee.summery', 'employee_id',
        string='Employment Summery', help='Employment Summery')
    employee_training_info_ids = fields.One2many(
        'hr.employee.training.info', 'employee_id',
        string='Employee Training Info', help='Employee Training Summery')

class EmploymentInfo(models.Model):
    _inherit = "hr.employee"

    designation_id = fields.Many2one('hr.employee.empdesignation', string='Designation')
    termination_date = fields.Date(string='Termination Date')
    emp_source_id = fields.Many2one('hr.employee.empsource', string='Employee Source')
    referred_by_id = fields.Many2one('hr.employee', string='Referred By')
    appointment_letter_provided = fields.Selection([
        ('yes', 'YES'),
        ('no', 'NO')], string='Appointment Letter Provided?', tracking=True)
    sim_eligibility = fields.Selection([
        ('yes', 'YES'),
        ('no', 'NO')], string='SIM Eligibility', tracking=True)
    
    sim_bundle_amount = fields.Float(string='SIM Bundle Amount', tracking=True)

class HrEmploymentSummery(models.Model):
    """Table to keep employee working summer"""

    _name = 'hr.employee.summery'
    _description = 'HR Employee summery'

    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  help='Select corresponding Employee',
                                  invisible=1)

    designation_id = fields.Many2one('hr.employee.empdesignation', string='Designation')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    service_length = fields.Char(string='Service Length',compute='_compute_service_length', tracking=True)
    increment_amount = fields.Float(string='Increment Amount')
    increment_percentage = fields.Float(string='Increment Percentage')
    promotion_date = fields.Date(string='Promotion Date')

    # @api.depends('start_date','end_date')
    # def _compute_service_length(self):
    #     for rec in self:
    #         # today = date.today()
    #         if rec.start_date and rec.end_date:
    #             rec.service_length =  (rec.end_date.year - rec.start_date.year)
    #         else:
    #             rec.service_length = 0 #if there is no else condition there will be a value error

    @api.depends('start_date','end_date')
    def _compute_service_length(self):
        for rec in self:
            # today = date.today()
            if rec.start_date and rec.end_date:
                rec.service_length =  "{value} months".format(value = (rec.end_date.year - rec.start_date.year) * 12 + rec.end_date.month - rec.start_date.month)
            else:
                rec.service_length = 0 
class HrEmployeeAcademicInfo(models.Model):
    """Table for keep employee academic information"""

    _name = 'hr.employee.academic'
    _description = 'HR Employee Academic'

    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  help='Select corresponding Employee',
                                  invisible=1)
    degree_title_id = fields.Many2one('hr.employee.degreetitle', String='Degree Title')
    degree_concentration_id = fields.Many2one('hr.employee.degreeconcentration', String='Concentration/Major/Group')
    board_name = fields.Selection([
        ('dhaka', 'Dhaka'),
        ('rajshahi', 'Rajshahi'),
        ('comilla', 'Comilla'),
        ('jessore', 'Jessore'),
        ('chittagong', 'Chittagong'),
        ('barisal', 'Barisal'),
        ('sylhet', 'Sylhet'),
        ('dinajpur', 'Dinajpur'),
        ('madrasah', 'Madrasah')],string='Board Name',tracking=True)

    degree_institute_id = fields.Many2one('hr.employee.degreeinstitute', string='Institute Name')
    gpa = fields.Char(string="GPA/Division", tracking=True)
    # year_of_passing = fields.Date(string="Year of Passing", tracking=True, format='%Y')
    country_id = fields.Many2one(
        'res.country', string='Country', tracking=True)

    @api.model
    def year_selection(self):
        year = 1980 # replace 2000 with your a start year
        year_list = []
        while year != 2030: # replace 2030 with your end year
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    year_of_passing = fields.Selection(
        year_selection,
        string="Year",
        default="2019", # as a default value it would be 2019
    )

class HrTrainingInfo(models.Model):
    """Table to keep employee training information"""

    _name = 'hr.employee.training.info'
    _description = 'HR Employee Training Info'

    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  help='Select corresponding Employee',
                                  invisible=1)
    training_title = fields.Char(string='Training Title')
    train_institute_id = fields.Char(string='Institute')
    train_location = fields.Char(String='Location')
    country_id = fields.Many2one('res.country', string='Country')
    training_year = fields.Date(string='Training Year')
    training_duration = fields.Char(string='Duration')
    training_facilator = fields.Char(string='Facilators Name')

class NomineeReferenceInfo(models.Model):
    _inherit = "hr.employee"

    nominee_name = fields.Char(string='Nominee Name', tracking=True)
    nominee_relation_id = fields.Many2one('hr.employee.relation',string='Relation')
    nominee_dob = fields.Date(string="Date of Birth", tracking=True)
    nominee_gen = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')],string='Gender',tracking=True)
    nominee_nid = fields.Char(string='Nominee NID')
    nominee_bid = fields.Char(string='Nominee Birth ID')
    nominee_present_add = fields.Char(string='Present Address')
    nominee_permanent_add = fields.Char(string='Permanent Address')
    nominee_email = fields.Char(string='Email')
    nominee_phone = fields.Char(string='Phone')
    nominee_mobile_banking = fields.Selection([
        ('bkash', 'Bkash'),
        ('nagad', 'Nagad'),
        ('others', 'Others')],string='Mobile Banking',tracking=True)

    nominee_mobile_banking_ac = fields.Char(string='Mobile Banking AC')
    reference_name = fields.Char(string='Reference Name', tracking=True)
    reference_rel = fields.Many2one('hr.employee.refrel',string='Relation with Reference',tracking=True)
    duration_of_knowing = fields.Date(string="Duration of Knowing",tracking=True)
    ref_present_add = fields.Char(string='Present Address')
    ref_permanent_add = fields.Char(string='Permanent Address')
    ref_occupation_id = fields.Many2one('hr.employee.occupation', string='Ocuppation')

class RefRelation(models.Model):
    _name = 'hr.employee.refrel'
    _rec_name = 'refrel'
    refrel = fields.Char(string="Relation with Reference",
                       help="What is relation with the reference person")    

class HrEmployeePrevEmpHistory(models.Model):
    """Table for keep employee previous employment history"""

    _name = 'hr.employee.previous.employment.history'
    _description = 'HR Employee Previous Employment History'

    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  help='Select corresponding Employee',
                                  invisible=1)

    previous_org_id = fields.Many2one('hr.employee.previousorganisation', string='Previous Organization')
    previous_desig_id = fields.Many2one('hr.employee.previousdesignation', string='Previous Designation')
    previous_dept_id = fields.Many2one('hr.employee.previousdepartment', string='Previous Department')
    previous_company_loc = fields.Char(string='Company location')
    prev_com_date_from = fields.Date(string='Date From')
    prev_com_date_to = fields.Date(string='Date To')




# class EmployeeFamily(models.Model):
#     _inherit = 'hr.employee.family'

#     nid_family = fields.Char(string="NID", tracking=True)
#     occupation_id = fields.Many2one(comodel_name='hr.employee.occupation',string="Occupation", tracking=True)




class DegreeTitle(models.Model):
    _name = 'hr.employee.degreetitle'
    _rec_name = 'degreetitle'
    degreetitle = fields.Char(string="Degree Title",
                       help="What type of degree you have")

class DegreeConcentration(models.Model):
    _name = 'hr.employee.degreeconcentration'
    _rec_name = 'degree_concentration'
    degree_concentration = fields.Char(string="Degree Concentration",
                       help="What type of degree you have")

class DegreeInstitute(models.Model):
    _name = 'hr.employee.degreeinstitute'
    _rec_name = 'degree_institute'
    degree_institute = fields.Char(string="Institue Name",
                       help="Name of your institue")

class PreviousOrganisation(models.Model):
    _name = 'hr.employee.previousorganisation'
    _rec_name = 'previous_org'
    previous_org = fields.Char(string="Previous Organisation",
                       help="What type of degree you have")

class PreviousDesignation(models.Model):
    _name = 'hr.employee.previousdesignation'
    _rec_name = 'previous_desig'
    previous_desig = fields.Char(string="Previous Designation",
                       help="What type of degree you have")

class PreviousDepartment(models.Model):
    _name = 'hr.employee.previousdepartment'
    _rec_name = 'previous_dept'
    previous_dept = fields.Char(string="Previous Department",
                       help="What type of degree you have")

class EmpDesignation(models.Model):
    _name = 'hr.employee.empdesignation'
    _rec_name = 'designation'

    designation = fields.Char(string="Designation")
    id = fields.Char(string="Designation ID")

class EmpSource(models.Model):
    _name = 'hr.employee.empsource'
    _rec_name = 'emp_source'

    emp_source = fields.Char(string="Source of Employee")
# class OccupationInfo(models.Model):
#     _name = 'hr.employee.occupation'
#     _rec_name = 'occupaton'
#     occupaton = fields.Char(string="Occupaton",
#                        help="What does the person do")