from datetime import date 

from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    state = fields.Selection(selection_add=[('draft','Purchase Order'),('sent','Purchase Order Sent'),('purchase','Proforma Invoice'),('lc_confirm', 'Letter of Credit Confirm'),('done',)],tracking=True,ondelete={'lc_confirm':'cascade'})
    order_date = fields.Date('Order Date', default=fields.Date.today())
    approx_arrive_date = fields.Date('Approx. Shipment Date', default=fields.Date.today())
    pi_date = fields.Date('Proforma Invoice Date', default=fields.Date.today())
    ship_mode = fields.Selection([
        ('sea', 'Sea'),
        ('air', 'Air'),
        ('road', 'Road')], 
        default='sea',
        string="Shipping Mode")
    discharge_port_id = fields.Many2one('scm.port',string="Discharge Port")
    ship_from_id = fields.Many2one('scm.ship',string="Ship From")
    incoterm = fields.Many2one(
        'account.incoterms', 'Incoterm',
        help="International Commercial Terms are a series of predefined commercial terms used in international transactions.")

    def action_in_lc(self):
        for rec in self:
            rec.state = 'lc_confirm'

    def action_in_lc_cancel(self):
        for rec in self:
            rec.state = 'purchase'

class PurchaseOrderLine(models.Model):
    _inherit = ['purchase.order.line']

    moq = fields.Float(
        'MOQ', default=0.0, required=True, digits="Product Unit Of Measure",
        help="The quantity to purchase from this vendor to benefit from the price, expressed in the vendor Product Unit of Measure if not any, in the default unit of measure of the product otherwise.")

    @api.onchange('product_id')
    def onchange_product_id(self):
        super(PurchaseOrderLine, self).onchange_product_id()
        if not self.product_id:
            return

        # Reset date, price and quantity since _onchange_quantity will provide default values
        self.moq = 0.0

        self._suggest_quantity()


    def _suggest_quantity(self):
        '''
        Suggest a minimal quantity based on the seller
        '''
        super(PurchaseOrderLine, self)._suggest_quantity()

        if not self.product_id:
            return
        seller_moq = self.product_id.seller_ids\
            .filtered(lambda r: r.name == self.order_id.partner_id and (not r.product_id or r.product_id == self.product_id))\
            .sorted(key=lambda r: r.moq)
        if seller_moq:
            self.moq = seller_moq[0].moq or 1.0
        else:
            self.moq = 1.0


class Port(models.Model):
    _name = "scm.port"
    _rec_name = 'discharge_port'

    discharge_port = fields.Char(string="Discharge Port")

class Ship(models.Model):
    _name = "scm.ship"
    _rec_name = 'ship_from'

    ship_from = fields.Char(string="Ship From")
