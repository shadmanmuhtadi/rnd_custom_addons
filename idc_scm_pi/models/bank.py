from odoo import api, fields, exceptions, models, SUPERUSER_ID, _
from odoo.exceptions import UserError


class bank(models.Model):
    _name = "scm.bank"
    _rec_name = "bank_name"

    bank_name = fields.Char(string = "Bank Name")
    swift_code = fields.Char(string = "Swift Code")

