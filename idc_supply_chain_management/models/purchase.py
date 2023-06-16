from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    state = fields.Selection(selection_add=[('draft','PO'),('sent','PO Sent'),('purchase','PI'),('lc_confirm', 'LC Confirm'),('done',)],tracking=True,ondelete={'lc_confirm':'cascade'})


    def action_in_lc(self):
        for rec in self:
            rec.state = 'lc_confirm'