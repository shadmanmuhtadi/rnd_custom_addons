from odoo import api, fields, models
import datetime


class AssignedDetails(models.Model):
    _name  = "assigned.details"
    _description = "Assigned Details"
    _rec_name = "assigned_id"

    assigned_id = fields.Many2one('product.template', string = "Product Name")
    assigned_to = fields.Many2one('hr.employee', string = "Assigned to", required=True)
    assigned_quantity = fields.Integer(string = "Quantity", default = 1, required=True)
    date = fields.Date(string = "Date", required=True)
    serial_id = fields.Many2many("serial.details", string = "Serial ID", required=True)

class ProductTemplate(models.Model):
    _inherit = "product.template"
    _description = "Product Template"
    
    date = fields.Date(string = "Date")
    vendor_name = fields.One2many('purchase.details','vendor_id', string = "Vendor Name")
    allocation_date =  fields.Date(string = "First Allocation Date")
    days_difference = fields.Char(string='Aging', compute="_compute_difference")
    document = fields.Binary(string='Upload Document')
    document_name = fields.Char(string="File Name")
    assigned_to = fields.One2many('assigned.details','assigned_id',string = "Assigned To")
    category = fields.Many2one(comodel_name ='recommendation.types',string = 'Category', required=True)
    quantity_new = fields.Char(string = 'On Hand Quantity', default=0, compute = "_compute_quantity")
    mac = fields.Char(string = 'MAC Address')
    assest = fields.Char(string = 'Assest ID', required=True)
    
    @api.depends("allocation_date")
    def _compute_difference(self):
        today_date = datetime.date.today()
        for rec in self:
            if rec.allocation_date:
                allocation_date = fields.Datetime.to_datetime(rec.allocation_date).date()
                total_day = (today_date - allocation_date)
                year = total_day.days//(365.25)
                month = (total_day.days-year*365.25)//(365.25/12)
                day = ((total_day.days-year*365.25) - month*(365.25/12))
                total_day = str(int(day)) + " Days " + str(int(month)) + " Months " + str(int(year)) + " Year"
                rec.days_difference = total_day
            else:
                rec.days_difference = "Not Available"

    @api.depends("assigned_to.assigned_quantity", "vendor_name.unit")
    def _compute_quantity(self):
        for record in self:
            total_buy = 0
            total_assign = 0
            for rec1 in record.assigned_to:
                    total_assign += rec1.assigned_quantity
            for rec2 in record.vendor_name:
                    total_buy += rec2.unit
            quantity = total_buy - total_assign
            record.quantity_new = quantity

       

class VendorDetails(models.Model):
    _name  = "vendor.details"
    _description = "Vendor Details"
    _rec_name = "vendor"

    vendor = fields.Char(string = "Vendor Name", required=True)
    vendor_person_number = fields.Char(string = "Contact Number")

class PurchaseDetails(models.Model):
    _name  = "purchase.details"
    _description = "Purchase Details"
    _rec_name = "vendor_id"

    vendor_id = fields.Many2one('product.template', string = "Product Name")
    vendor_name = fields.Many2one("vendor.details", string = "Vendor Name", required=True)
    price = fields.Float(string = "Unit Price", default = 0, required=True)
    unit = fields.Integer(string="Unit", default = 1, required=True)
    date = fields.Date(string = "Date", required=True)
    total_price = fields.Float(string = "Total Price", default = 0, compute="_compute_total_price")
    @api.depends("price","unit")
    def _compute_total_price(self):
        for rec in self:
            if rec.unit and rec.price:
                total_price = rec.unit * rec.price
                rec.total_price = total_price
            else:
                rec.total_price = 0

class SerialDetails(models.Model):
    _name  = "serial.details"
    _description = "Serial Details"
    _rec_name = "serial"
    serial = fields.Integer(string = "Serial ID", required=True)