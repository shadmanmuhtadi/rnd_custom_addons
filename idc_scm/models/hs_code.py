from odoo import api, fields, models

class hscode(models.Model):

    _name = "scm.hscode"
    _description = "HSCode"
    _rec_name = 'hs_code'

    hs_code = fields.Char(string='HS Code', required= True)
    insurance = fields.Float(string='Insurance')
    landing = fields.Float(string='Landing')
    assvalue = fields.Float(string='Assesment Value', compute ='_compute_assvalue')
    cd = fields.Float(string='Continuous Delivery')
    rd = fields.Float(string='RD')
    sd = fields.Float(string='Store Door')
    vat = fields.Float(string='VAT')
    ait = fields.Float(string='AIT')
    at = fields.Float(string='AT')
    total_tti = fields.Float(string='TTI', compute ='_compute_total_tti')

#Computation of Assesment Value
    @api.depends('insurance','landing')
    def _compute_assvalue(self):
        for record in self:
            record.assvalue = (
                    (1+(1*(record.insurance)))
                    +(1+(1*(record.insurance)))*(record.landing)
                    )*100

#Computation of TTI Value    
    @api.depends('assvalue', 'cd', 'rd', 'sd', 'vat', 'ait', 'at')
    def _compute_total_tti(self):
        for record in self:
            # Perform the calculation logic here
            record.total_tti = (
                (record.assvalue * record.cd ) +
                (record.assvalue * record.rd ) +
                ((record.assvalue + (record.assvalue * record.cd) + (record.assvalue * record.rd)) * record.sd) +
                ((record.assvalue + (record.assvalue * record.cd) + (record.assvalue * record.rd) + (record.assvalue + (record.assvalue * record.cd) + (record.assvalue * record.rd)) * record.sd) * record.vat) +
                (record.assvalue + record.ait) +
                ((record.assvalue + (record.assvalue * record.cd) + (record.assvalue * record.rd) + (record.assvalue + (record.assvalue * record.cd) + (record.assvalue * record.rd)) * record.sd) * record.at)
            )
