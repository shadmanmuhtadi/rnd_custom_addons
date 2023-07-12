
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }
    
    # po_id = fields.Many2one('purchase.order.pi', string='Purchase Order')

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
