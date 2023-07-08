from datetime import date 

from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    state = fields.Selection(selection_add=[('draft','Purchase Order'),('sent','Purchase Order Sent'),('purchase','Proforma Invoice'),('lc_confirm', 'Letter of Credit Confirm'),('done', 'Done')],tracking=True,ondelete={'lc_confirm':'cascade'})
    order_date = fields.Date('Order Date', default=fields.Date.today())
    approx_arrive_date = fields.Date('Approx. Shipment Date', default=fields.Date.today())
    pi_date = fields.Date('Proforma Invoice Date', default=fields.Date.today())
    ship_mode = fields.Selection([
        ('sea', 'Sea'),
        ('air', 'Air'),
        ('road', 'Road')], 
        default='sea',
        string="Ship Mode")
    discharge_port_id = fields.Many2one('scm.port',string="Discharge Port")
    ship_from_id = fields.Many2one('scm.ship',string="Ship From")
    incoterm = fields.Many2one(
        'account.incoterms', 'Incoterm',
        help="International Commercial Terms are a series of predefined commercial terms used in international transactions.")



    def action_in_lc(self):
        for rec in self:
            rec.state = 'lc_confirm'


class Port(models.Model):
    _name = "scm.port"

    discharge_port = fields.Char(string="Discharge Port")

class Ship(models.Model):
    _name = "scm.ship"

    ship_from = fields.Char(string="Ship From")