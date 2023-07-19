from odoo import api, fields, exceptions, models, SUPERUSER_ID, _
from odoo.exceptions import UserError


class PurchasePo(models.Model):
    _name = "purchase.po"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Purchase Order"
    _order = 'id desc'
    _rec_name = 'ref'


    ref = fields.Char(string='PO Reference', default=lambda self: self._get_next_purchaseref(), store=True, readonly=True)
    company_id = fields.Many2one('res.company', 'Company', copy=False,default=lambda self: self.env.company,readonly=True)
    po_lines = fields.One2many('purchase.po.line', 'po_id', string='Purchase order Lines', copy=True)
    order_date = fields.Datetime('Order Date', required=True, index=True, copy=False, )
    partner_id = fields.Many2one('res.partner', string='Partner', store=True)

    pi_lines = fields.One2many('purchase.pi','po_id', string='', copy=False)
    pi_count = fields.Integer(compute="_compute_purchase_orders", string='PI Count', copy=False, default=0, store=True)

    @api.model
    def _get_next_purchaseref(self):
        sequence = self.env['ir.sequence'].search([('code','=','purchase.po')])
        next= sequence.get_next_char(sequence.number_next_actual)
        return next

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('purchase.po')
        result = super(PurchasePo, self).create(vals)
        return result
    
#-------------------------------------------------------------------------
    def _create_pi_lines_context(self, pi_ids):
        lines = []
        for line in self.po_lines:
            if line.product_qty > 0:
                lines.append((
                    0, 0, {
                        'product_id': line.product_id.id,
                        'product_qty': line.product_qty,
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
    def _compute_purchase_orders(self):
        for order in self:
            pis = order.mapped('pi_lines')
            order.pi_count = len(pis)
    
    
    
class PurchasePoLine(models.Model):
    _name = 'purchase.po.line'

    po_id = fields.Many2one('purchase.po', string='Order Reference', index=True, required=True,
                                  ondelete='cascade')

    product_id = fields.Many2one('product.product', string='Product', change_default=True)
    product_uom = fields.Many2one('uom.uom', related='product_id.uom_id', string='Unit of Measure', )
    price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price')
    product_packaging_id = fields.Many2one('product.packaging', string='Packaging', domain="[('purchase', '=', True), ('product_id', '=', product_id)]", check_company=True)


    product_qty = fields.Float(string='Qty', digits='Product Unit of Measure', required=True)