from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order.shipment']

    net_weight = fields.Float(string='')
    gross_weight = fields.Float(string='')
    cbm = fields.Float(string='CBM')
    bl_no = fields.Char(string='B/L No')
    container_qty = fields.Float(string='')
    port_arrival_date = fields.Date(string='')
    lc_no = fields.Char(string='')
    invoice_no = fields.Char(string='')
    invoice_date = fields.Date(string='')

    