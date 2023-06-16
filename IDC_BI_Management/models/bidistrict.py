from odoo import api, fields, models

class BiDistrict(models.Model):
    _name = "bi.district"
    _description = "Bi District"

    reportname = fields.Char(string = "Report Name")
    reportlink = fields.Char(String = "Report Link")
    