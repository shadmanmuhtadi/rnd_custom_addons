
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }
    
    pi_ids = fields.One2many('purchase.pi','purchase_id', string='Proforma Invoices Order')

    @api.onchange('pi_ids')
    def _onchange_pi_ids(self):
        #without this validation order line adds under previous line
        # if self.order_line: 
        #     raise UserError(
        #         _(
        #             "Please remove lines and select Purchase Order again "
        #         )
        #     )
        if self.pi_ids:
            order_line = self.pi_ids._create_purchase_order_lines_context(self.pi_ids.pi_lines)
            self.order_line = order_line
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
