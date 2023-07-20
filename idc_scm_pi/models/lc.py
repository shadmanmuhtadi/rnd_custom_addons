
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
logger = logging.getLogger("Your Message")

class lc(models.Model):
    _inherit = 'purchase.order'
    

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }
    
    pi_ids = fields.One2many('purchase.pi','lc_id', string='Proforma Invoices')

    #based on the selected pi_ids the orderline gets populated
    @api.onchange('pi_ids')
    def _onchange_pi_ids(self):
        if self.pi_ids:
            order_line = self.pi_ids._create_lc_lines_context(self.pi_ids.order_line)
            self.order_line = order_line


#to sum up the duplicate sku quantity in lc
class purchase_order_line(models.Model):
    _inherit = 'purchase.order.line'

    @api.model
    def create(self, vals):
        same_line = self.search([('product_id', '=', vals.get('product_id', False)),
                                ('order_id', '=', vals.get('order_id', False))])
        if same_line:
            total_qty = same_line.product_qty + vals.get('product_qty', 0)
            vals.update({
                'product_qty': total_qty,
            })
            same_line.write(vals)
            return same_line
        else:
            return super(purchase_order_line, self).create(vals)

    #check them in comunity purchase.order model
    
    # partner_id = fields.Many2one('res.partner',
    #                              string='Vendor', required=True,
    #                              states=READONLY_STATES,
    #                              related='po_id.partner_id',
    #                              change_default=True, tracking=True,
    #                              domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    #                              help="You can find a vendor by its Name, TIN, Email or Internal Reference.")


    # company_id = fields.Many2one('res.company','Company',
    #                              required=True,
    #                              readonly=True,
    #                              related='po_id.company_id',
    #                              index=True,states=READONLY_STATES,
    #                              default=lambda self: self.env.company.id)
