from odoo import api, fields, models

class BiKmd(models.Model):
    _name = "bi.kmd"
    _description = "Bi Kmd"

    reportname = fields.Char(string = "Report Name")
    reportlink = fields.Char(String = "Report Link")
    