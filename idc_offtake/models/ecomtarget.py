from odoo import api, fields, models

class EcomTarget(models.Model):
    _name = "ecom.target"
    _description = "ECOM Target"

    date = fields.Date(string = "Date")
    level1 = fields.Char(String = "Level 1")
    level1name = fields.Char(String = "Level 1 Name")
    custtypename = fields.Char(String = "Cust Type Name")
    customercode = fields.Char(String = "Customer Code")
    customername = fields.Char(String = "Customer Name")
    subbusiness = fields.Char(String = "Sub Business")
    category = fields.Char(String = "Category")
    productcode = fields.Char(String = "Product Code")
    productname = fields.Char(String = "Product Name")
    tp = fields.Float(String = "TP")
    qty = fields.Integer(String = "QTY")
    value = fields.Float(String = "Value")
    brand = fields.Char(String = "Brand")
    keyaccount = fields.Char(String = "Key Account")

   