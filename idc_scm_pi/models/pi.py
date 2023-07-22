

from odoo import api, fields, exceptions, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
import logging
logger = logging.getLogger("Your Message")


class PurhcasePi(models.Model):
    _name = "purchase.pi"
    _inherit = ['purchase.order','mail.thread', 'mail.activity.mixin']
    _description = "Purchase po"

    READONLY_STATES = {
            'purchase': [('readonly', True)],
            'done': [('readonly', True)],
            'cancel': [('readonly', True)],
        }

    state = fields.Selection([
        ('draft', 'Draft'),
        ('to approve', 'To Approve'),
        ('sent', 'Approved'),
        ('purchase', 'PI Received'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    partner_id = fields.Many2one('res.partner', related='po_id.partner_id', string='Vendor', required=True, states=READONLY_STATES, change_default=True, tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
    date_order = fields.Datetime('Order Date', related='po_id.date_order', required=True, states=READONLY_STATES, index=True, copy=False)
    date_planned = fields.Datetime(
        string='Receipt Date', index=True, related='po_id.date_planned', copy=False, compute='_compute_date_planned', store=True, readonly=False,
        help="Delivery date promised by vendor. This date is used to determine expected arrival of products.")
    order_line = fields.One2many('purchase.pi.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)
    po_id = fields.Many2one('purchase.po', string='Purchase Order')

    lc_id = fields.Many2one('purchase.order', string='LC')

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
    #send the pi lines to lc lines
    def _create_lc_lines_context(self, lc_id):
        #lines = [(5,0,0)] clear up previously selected order line 
        lines = [(5,0,0)]
        for line in self.order_line:
            if line.product_qty > 0:
                lines.append((
                    0, 0, {
                        'product_id': line.product_id.id,
                        'name': line.name,
                        'product_uom':line.product_uom,
                        'price_unit':line.price_unit,
                        'price_subtotal':line.price_subtotal,
                        'product_qty': line.product_qty,
                    }
                ))
            else:
                continue
        return lines
    
#------------------------------------------------
#---------------------------------------------------------------------

    @api.onchange('po_id')
    def _onchange_po_id(self):
        if self.order_line: #without this validation order line adds under previous line
            raise UserError(
                _(
                    "Please remove lines and select Purchase Order again "
                )
            )
        if self.po_id:
            order_line = self.po_id._create_pi_lines_context(self.po_id.pi_lines)
            self.order_line = order_line
#--------------------------------------------------------------------------

    #sequence for pi
    @api.model
    def create(self, vals):
        company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
        # Ensures default picking type and currency are taken from the right company.
        self_comp = self.with_company(company_id)
        if vals.get('name', 'New') == 'New':
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
            vals['name'] = self_comp.env['ir.sequence'].next_by_code('purchase.pi', sequence_date=seq_date) or '/'
        vals, partner_vals = self._write_partner_values(vals)
        res = super(PurhcasePi, self_comp).create(vals)
        if partner_vals:
            res.sudo().write(partner_vals)  # Because the purchase user doesn't have write on `res.partner`
        return res

class PurhcasePiline(models.Model):
    _name = "purchase.pi.line"
    _inherit = ['purchase.order.line']
    _description = "Purchase order pi line"


    order_id = fields.Many2one('purchase.pi', string='Order Reference', index=True, required=True, ondelete='cascade')
    product_qty = fields.Float(string='Quantity Approved', digits='Product Unit of Measure', required=True)
    qty_ordered = fields.Float(string='Ordered Quantity')


