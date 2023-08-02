from odoo import api, fields, models


class PayrollInfo(models.Model):
    _inherit = "hr.contract"

    bank_name_id = fields.Many2one('hr.employee.bankname', string='Bank Name')
    bank_account_num = fields.Char(string='Bank Account Number')
    mobile_banking = fields.Selection([
        ('bkash', 'Bkash'),
        ('nagad', 'Nagad'),
        ('upay', 'Upay'),
        ('rocket', 'Rocket'),
        ('surecash', 'SureCash')],tracking=True)
    mobile_banking_num = fields.Char(string='Mobile Banking Num',tracking=True)

    cash = fields.Boolean(string='Cash')


class BankName(models.Model):
    _name = 'hr.employee.bankname'
    _rec_name = 'bank_name'
    bank_name = fields.Char(string="bank name",
                       help="select the bank name")