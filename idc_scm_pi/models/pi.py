from odoo import api, fields, exceptions, models, SUPERUSER_ID, _
from odoo.exceptions import UserError


class PurhcasePi(models.Model):
    _name = "purchase.pi"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Proforma Invoice"
    _order = 'id desc'
    _rec_name = 'ref'


    ref = fields.Char(string='PI Reference', default=lambda self: self._get_next_purchaseref(), store=True, readonly=True)
    company_id = fields.Many2one('res.company', 'Company', copy=False,default=lambda self: self.env.company,readonly=True)
    pi_lines = fields.One2many('purchase.pi.line', 'pi_id', string='Purchase order Lines', copy=True)
    
    po_id = fields.Many2one('purchase.po', string='Purchase Order')

    pi_date = fields.Datetime('Order Date', required=True, index=True, copy=False, )
    partner_id = fields.Many2one('res.partner', related='po_id.partner_id', string='Partner', store=True)


    purchase_id = fields.Many2one('purchase.order', string='Purchase')
    #-------------------------------------------------------------------------

    def _create_purchase_order_lines_context(self, purchase_id):
        lines = []
        for line in self.pi_lines:
            if line.product_qty > 0:
                lines.append((
                    0, 0, {
                        'product_id': line.product_id.id,
                        'product_qty': line.qty_approved,
                    }
                ))
            else:
                continue
        return lines
    
#----------------------------------------------------------------------------   
#---------------------------------------------------------------------

    @api.onchange('po_id')
    def _onchange_po_id(self):
        if self.pi_lines: #without this validation order line adds under previous line
            raise UserError(
                _(
                    "Please remove lines and select Purchase Order again "
                )
            )
        if self.po_id:
            pi_lines = self.po_id._create_pi_lines_context(self.po_id.pi_lines)
            self.pi_lines = pi_lines
#--------------------------------------------------------------------------
    @api.model
    def _get_next_purchaseref(self):
        sequence = self.env['ir.sequence'].search([('code','=','purchase.pi')])
        next= sequence.get_next_char(sequence.number_next_actual)
        return next

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('purchase.pi')
        result = super(PurhcasePi, self).create(vals)
        return result
    
    
    
class PurhcasePiLine(models.Model):
    _name = 'purchase.pi.line'

    pi_id = fields.Many2one('purchase.pi', string='Order Reference', index=True, required=True,
                                  ondelete='cascade')


    product_id = fields.Many2one('product.product', string='Product', change_default=True)
    product_uom = fields.Many2one('uom.uom', related='product_id.uom_id', string='Unit of Measure', )
    price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price')
    product_packaging_id = fields.Many2one('product.packaging', string='Packaging', domain="[('purchase', '=', True), ('product_id', '=', product_id)]", check_company=True)
    product_qty = fields.Float(string='Ordered Qty', digits='Product Unit of Measure', required=True)
    qty_approved = fields.Float(string='Approved Qty')
    remaining_qty = fields.Float(string='Remaining Qty')