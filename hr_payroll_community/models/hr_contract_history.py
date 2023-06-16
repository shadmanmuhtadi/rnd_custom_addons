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
    _description = 'Employee Contract history'

    total_salary = fields.Float(string="Total Salary")
