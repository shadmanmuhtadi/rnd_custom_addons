from odoo import api, fields, exceptions, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
import datetime
import logging
logger = logging.getLogger("Your Message")


class PurhcasePo(models.Model):
    _name = "purchase.po"
    _inherit = ['purchase.order','mail.thread', 'mail.activity.mixin']
    _description = "Purchase PO"
    _rec_name = 'custom_po_ref'

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }
    custom_po_ref = fields.Char(string="Purchase Order No", readonly=True, index=True, default='New')

    order_type = fields.Selection([
        ('IMP', 'Import'),
        ('LP', 'Local'),
        ('3P', 'Third Party'),
        ('OT', 'Others'),
    ], string='Order Type', index=True, copy=False, default='import', tracking=True, required=True)
    ship_mode = fields.Selection([
        ('sea', 'Sea'),
        ('air', 'Air'),
        ('road', 'Road')], 
        default='sea',
        string="Ship Mode")
    
    partner_ref = fields.Char('Supplier Reference', copy=False,
        help="Reference of the sales order or bid sent by the vendor. "
             "It's used to do the matching when you receive the "
             "products as this reference is usually written on the "
             "delivery order sent by your vendor.")
    
    order_date = fields.Date('Order Date', default=fields.Date.today())
    approx_shipment_date = fields.Date('Approx. Shipment Date', default=fields.Date.today())
    approx_arrival_month = fields.Date('Approx. Arrival Month', default=fields.Date.today())

    partner_id = fields.Many2one('res.partner', string='Supplier', required=True, states=READONLY_STATES, change_default=True, tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
    vendor_code = fields.Char(related='partner_id.vendor_code', string='vendor code',store=True)
    discharge_port_id = fields.Many2one('scm.port',string="Discharge Port")
    ship_from_id = fields.Many2one('scm.ship',string="Ship From")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('to approve', 'To Approve'),
        ('sent', 'Approved'),
        ('purchase', 'PI Received'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    order_line = fields.One2many('purchase.po.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)

    pi_lines = fields.One2many('purchase.pi','po_id', string='', copy=False)
    pi_count = fields.Integer(compute="_compute_pi_orders", string='PI Count', copy=False, default=0, store=True)

    def button_confirm(self):
        for rec in self:
            rec.state = 'purchase'
    
    def button_approve(self):
        for rec in self:
            rec.state = 'sent'
    def button_done(self):
        for rec in self:
            rec.state = 'done'
    def button_cancel(self):
        for rec in self:
            rec.state = 'cancel'

#-------------------------------------------------------------------------
    def _create_pi_lines_context(self, pi_ids):
        lines = []
        for line in self.order_line:
            if line.product_qty > 0:
                lines.append((
                    0, 0, {
                        'product_id': line.product_id.id,
                        'name': line.name,
                        'product_uom':line.product_uom,
                        'price_unit':line.price_unit,
                        'price_subtotal':line.price_subtotal,
                        'qty_ordered': line.product_qty, #sending the quantity in order quantity, in product_qty user will put the approved quantity, which will go to lc lines
                    }
                ))
            else:
                continue
        return lines
#----------------------------------------------------------------------------    
    def action_open_pi(self):
        pi_ids = self.mapped('pi_lines')
        domain = "[('id','in',%s)]" % (pi_ids.ids)
        context = {
            'default_po_id': self.id,
        }
        return {
            'name': _("Proforma Invoices"),
            'view_mode': 'tree,form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'purchase.pi',
            'type': 'ir.actions.act_window',
            'domain': domain,
            'context': context
        }
    
    @api.depends('pi_lines')
    def _compute_pi_orders(self):
        for order in self:
            pis = order.mapped('pi_lines')
            order.pi_count = len(pis)

    #sequence for po
    @api.model
    def create(self, vals):
        company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
        # Ensures default picking type and currency are taken from the right company.
        self_comp = self.with_company(company_id)
        if vals.get('name', 'New') == 'New':
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
            vals['name'] = self_comp.env['ir.sequence'].next_by_code('purchase.po', sequence_date=seq_date) or '/'
        vals, partner_vals = self._write_partner_values(vals)
        res = super(PurhcasePo, self_comp).create(vals)
        if partner_vals:
            res.sudo().write(partner_vals)  # Because the purchase user doesn't have write on `res.partner`
        return res
    

    #po custom ref generator
    @api.model
    def create(self, vals):
        serial_no = self.env['ir.sequence'].get('purchase.po.customized.sequence')
        supplier_code = self.env['res.partner'].browse(vals['partner_id']).vendor_code
        if supplier_code is False:
            raise UserError("Supplier short code is not available!!")
        vals['custom_po_ref'] = vals.get('order_type') + '/' + supplier_code + '/' + str(datetime.datetime.now().year) + '/'+ str(datetime.datetime.now().month) + '/' + serial_no
        return super(PurhcasePo, self).create(vals)
    
    @api.depends('order_line.date_planned')
    def _compute_date_planned(self):
        """ date_planned = the earliest date_planned across all order lines. """
        for order in self:
            dates_list = order.order_line.filtered(lambda x: not x.display_type and x.date_planned).mapped('date_planned')
            if dates_list:
                order.date_planned = fields.Datetime.to_string(min(dates_list))
            else:
                order.date_planned = False

#---------------------------------


class PurhcasePoline(models.Model):
    _name = "purchase.po.line"
    _inherit = ['purchase.order.line']
    _description = "Purchase po order line"


    order_id = fields.Many2one('purchase.po', string='Order Reference', index=True, required=True, ondelete='cascade')
    moq = fields.Float(
        'MOQ', default=0.0, required=True, digits="Product Unit Of Measure",
        help="The quantity to purchase from this vendor to benefit from the price, expressed in the vendor Product Unit of Measure if not any, in the default unit of measure of the product otherwise.")
    product_qty = fields.Float(string='Qunatity In Pack', digits='Product Unit of Measure', required=True)
    price_unit = fields.Float(string='Pack Price', required=True, digits='Product Price')

    @api.onchange('product_id')
    def onchange_product_id(self):
        super(PurhcasePoline, self).onchange_product_id()
        if not self.product_id:
            return

        # Reset date, price and quantity since _onchange_quantity will provide default values
        self.moq = 0.0

        self._suggest_quantity()


    def _suggest_quantity(self):
        '''
        Suggest a minimal quantity based on the seller
        '''
        super(PurhcasePoline, self)._suggest_quantity()

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