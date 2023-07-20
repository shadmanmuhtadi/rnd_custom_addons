

from odoo import api, fields, exceptions, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
import logging
logger = logging.getLogger("Your Message")


class PurhcasePo(models.Model):
    _name = "purchase.po"
    _inherit = ['purchase.order','mail.thread', 'mail.activity.mixin']
    _description = "Purchase PO"

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    partner_id = fields.Many2one('res.partner', string='Supplier', required=True, states=READONLY_STATES, change_default=True, tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
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

class PurhcasePoline(models.Model):
    _name = "purchase.po.line"
    _inherit = ['purchase.order.line']
    _description = "Purchase po order line"


    order_id = fields.Many2one('purchase.po', string='Order Reference', index=True, required=True, ondelete='cascade')

