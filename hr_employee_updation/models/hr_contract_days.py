
from odoo import models, fields, api, _
from datetime import date, timedelta


class HrEmployeeContract(models.Model):
    _inherit = 'hr.contract'

    def _get_default_notice_days(self):
        if self.env['ir.config_parameter'].get_param(
                'hr_resignation.notice_period'):
            return self.env['ir.config_parameter'].get_param(
                            'hr_resignation.no_of_days')
        else:
            return 0

    notice_days = fields.Integer(string="Notice Period",
                                 default=_get_default_notice_days)
    probation_period = fields.Integer(string="Porbation Period")
    confirmation_date = fields.Date(string="Confirmation Date",compute='_compute_confirmation_date', store=True)

    @api.depends('date_start','probation_period')
    def _compute_confirmation_date(self):
        for rec in self:
            rec.confirmation_date = rec.date_start + timedelta(rec.probation_period)
