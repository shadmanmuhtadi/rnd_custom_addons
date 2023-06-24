from odoo import api, fields, models

class FdnTarget(models.Model):
    _name = "fdn.target"
    _description = "FDN Target"

    date = fields.Date(string = "Date")
    level1 = fields.Char(string = "Level 1")
    level1name = fields.Char(string = "Level 1 Name")
    custtypename = fields.Char(string = "Cust Type Name")
    customercode = fields.Char(string = "Customer Code")
    customername = fields.Char(string = "Customer Name")
    subbusiness = fields.Char(string = "Sub Business")
    category = fields.Char(string = "Category")
    productcode = fields.Char(string = "Product Code")
    productname = fields.Char(string = "Product Name")
    tp = fields.Float(string = "TP")
    qty = fields.Integer(string = "QTY")
    value = fields.Float(string = "Value")
    brand = fields.Char(string = "Brand")
    keyaccount = fields.Char(string = "Key Account")