from odoo import api, fields, models

class AllOfftake(models.Model):
    _name = "all.offtake"
    _description = "All Offtake"

    date = fields.Date(string = "Date")
    customercode = fields.Char(String = "Customer Code")
    custtypename = fields.Char(String = "Cust Type Name")
    customername = fields.Char(String = "Customer Name")
    productcode = fields.Char(String = "Product Code")
    productname = fields.Char(String = "Product Name")
    subbusiness = fields.Char(String = "Sub Business")
    category = fields.Char(String = "Category")
    tp = fields.Float(String = "TP")
    offtakeqty = fields.Integer(String = "Offtake QTY")
    offtakevalue = fields.Float(String = "Offtake Value")
    stockqty = fields.Integer(String = "Stock QTY")
    stockvalue = fields.Float(String = "Stock Value")
    brand = fields.Char(String = "Brand")
    keyaccount = fields.Char(String = "Key Account")
    