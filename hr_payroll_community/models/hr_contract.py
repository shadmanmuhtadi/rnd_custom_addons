# -*- coding:utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
import logging #helps to print message in log
logger = logging.getLogger("*__Test log Message__:*") #helps to print messages in log

class HrContract(models.Model):
    """
    Employee contract based on the visa, work permits
    allows to configure different Salary structure
    """
    _inherit = 'hr.contract'
    _description = 'Employee Contract'

    struct_id = fields.Many2one('hr.payroll.structure', string='Salary Structure')
    basic = fields.Monetary(string="Basic Allowence")
    house_rent = fields.Monetary(string="House Allowence")
    med_allow = fields.Monetary(string="Medical Allowence")
    trans_allow = fields.Monetary(string="Transport Allowence")
    total_salary = fields.Monetary(string="Total Salary")
    schedule_pay = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi-annually', 'Semi-annually'),
        ('annually', 'Annually'),
        ('weekly', 'Weekly'),
        ('bi-weekly', 'Bi-weekly'),
        ('bi-monthly', 'Bi-monthly'),
    ], string='Scheduled Pay', index=True, default='monthly',
        help="Defines the frequency of the wage payment.")
    resource_calendar_id = fields.Many2one(required=True, help="Employee's working schedule.")
    hra = fields.Monetary(string='HRA', tracking=True, help="House rent allowance.")
    travel_allowance = fields.Monetary(string="Travel Allowance", help="Travel allowance")
    da = fields.Monetary(string="DA", help="Dearness allowance")
    meal_allowance = fields.Monetary(string="Meal Allowance", help="Meal allowance")
    medical_allowance = fields.Monetary(string="Medical Allowance", help="Medical allowance")
    other_allowance = fields.Monetary(string="Other Allowance", help="Other allowances")

    #total_salary will be calculated based the selection of salary structure
    @api.onchange('struct_id')
    def onchange_struct_id(self):
        summ = 0
        for rec in (self.struct_id.rule_ids):
            logger.info(f" Here is the message {rec.amount_fix}") #print message in log file
            logger.info(f" Here is the message {rec}") #print message in log file
            if rec.code == "Basic":
                self.basic = rec.amount_fix
            elif rec.code == "House":
                self.house_rent = rec.amount_fix
            elif rec.code == "Medical":
                self.med_allow = rec.amount_fix
            elif rec.code == "travel":
                self.trans_allow = rec.amount_fix
            logger.info(f" Here is the message {summ}") #print message in log file

            summ = summ + rec.amount_fix
        self.total_salary = summ

    #wage will update based on the change on total_salary
    @api.onchange('total_salary')
    def onchange_total_salary(self):
        self.wage = self.total_salary


            # self.basic = rec.amount_fix
        # for rec in (self.struct_id)
        #     logger.info(f"Inputed date of birth is {rec.rule_ids}") #print message in log file
    

    def get_all_structures(self):

        """
        @return: the structures linked to the given contracts, ordered by hierachy (parent=False first,
                 then first level children and so on) and without duplicata
        """
        structures = self.mapped('struct_id')
        if not structures:
            return []
        # YTI TODO return browse records
        return list(set(structures._get_parent_structure().ids))

    def get_attribute(self, code, attribute):

        return self.env['hr.contract.advantage.template'].search([('code', '=', code)], limit=1)[attribute]

    def set_attribute_value(self, code, active):
        for contract in self:

            if active:

                value = self.env['hr.contract.advantage.template'].search([('code', '=', code)], limit=1).default_value
                contract[code] = value
            else:

                contract[code] = 0.0


class HrContractAdvandageTemplate(models.Model):
    _name = 'hr.contract.advantage.template'
    _description = "Employee's Advantage on Contract"

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    lower_bound = fields.Float('Lower Bound', help="Lower bound authorized by the employer for this advantage")
    upper_bound = fields.Float('Upper Bound', help="Upper bound authorized by the employer for this advantage")
    default_value = fields.Float('Default value for this advantage')
