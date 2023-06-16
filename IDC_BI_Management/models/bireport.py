from odoo import api, fields, models

class BiReport(models.Model):
    _name = "bi.report"
    _description = "Bi Report"

    reportname = fields.Char(string = "Report Name")
    reportlink = fields.Char(String = "Report Link")
    