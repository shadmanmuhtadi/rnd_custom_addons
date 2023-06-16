from odoo import api, fields, models

class BiFdn(models.Model):
    _name = "bi.fdn"
    _description = "Bi FDN"

    reportname = fields.Char(string = "Report Name")
    reportlink = fields.Char(String = "Report Link")
    