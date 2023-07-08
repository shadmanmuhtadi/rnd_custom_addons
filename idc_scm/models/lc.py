from odoo import api, fields, models

class lc(models.Model):

    _name = "scm.lc"
    # _inherit = ['mail.thread','ir.attachment']
    _inherit = ['mail.thread']

    _description = "LC"
    _rec_name = 'lc_no'
   
    lc_date = fields.Datetime(string="LC Date",tracking=True, default=fields.Datetime.now)
    subtotal = fields.Float(readonly='1', compute='_compute_subtotal',string='Subtotal')
    notes = fields.Html('Terms and Conditions')
    lc_no = fields.Char(string='LC No')
    partner_id = fields.Many2one('res.partner', string='Principle', store=True)
    bank_name_id = fields.Many2one('scm.bank', string="Bank Name")

    shipment_date = fields.Datetime(string="Approx. Shipment Date", tracking=True)
    arrival_date = fields.Datetime(string="Approx. Arrival Date", tracking=True)
    branch_lc_sl_no = fields.Char(string="Branch LC SL No")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancel')], string='Status', default='draft')

    # attachments = fields.Many2many('ir.attachment', string="Attachments")
    
    order_lc_ids = fields.One2many('scm.order.lc','lc_id', string= "PI No")
    #---------------------------------------------------------------------

    @api.depends('order_lc_ids.amount_total')
    def _compute_subtotal(self):
        for order in self:
            subtotal = 0.0
            for line in order.order_lc_ids:
                subtotal = subtotal + line.amount_total
            order.subtotal = subtotal
    #----------------------------------------------------------------------------

    @api.model
    def create(self, vals):
        vals['lc_no'] = self.env['ir.sequence'].next_by_code('scm.lc')
        return super(lc, self).create(vals)
    
    def write(self, vals):
        if not self.lc_no and not vals.get('lc_no'):
            vals['lc_no'] = self.env['ir.sequence'].next_by_code('scm.lc')
        return super(lc, self).write(vals)

    def action_in_progress(self):
        for rec in self:
            rec.state = 'in_progress'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'
    
class order_lc(models.Model):
    _name = "scm.order.lc"
    _description = "Purchase LC"
    _rec_name = "order_id"


    order_id = fields.Many2one('purchase.order', domain="[('state', '=', 'purchase')]" ,string="Order Id")
    # amount_total = fields.Monetary(string='Order Value', related='order_id.amount_total')
    currency_id = fields.Many2one("res.currency", string="Valuta")
    amount_total = fields.Monetary(currency_field="currency_id",string='Total',related='order_id.amount_total')
    principle = fields.Many2one(string='Principles',related='order_id.partner_id')
    # selected_order_id = fields.Many2one('scm.purchase', string='Selected Product')
    # order_no_lc = fields.Integer(string="Order No")
    # shipment_date_lc = fields.Datetime(string="Approx. Shipment Date")
    # supplier_name = fields.Many2one('scm.vendor',string="Supplier Name")
    # supplier_id_lc = fields.Many2one('res.users',string="Supplier ID")

    lc_id = fields.Many2one('scm.lc',string='lc_id')


class Bank(models.Model):
    _name = "scm.bank"

    bank_name = fields.Char(string="Bank Name")

