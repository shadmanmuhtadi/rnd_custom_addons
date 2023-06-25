from odoo import api, fields, models

class ProductTemplate(models.Model):

    _inherit = ['product.template']


    sub_business = fields.Many2one('product.category', string='Sub Business', help='For example: Modelez')
    brand = fields.Many2one('product.category', string='Brand',help='For example: Tang, cadbury')
    category = fields.Many2one('product.category', string='Category',help='For example: Silk')
    master_code = fields.Char(string='Master Code',help='Might be provided by Principles')
    regulatory_issue = fields.Selection([('bsti', 'BSTI'), ('bcsir','BCSIR')], string="Regulatory Issue", default='bsti')
    bsti_no = fields.Char('BSTI No')
    country_id = fields.Many2one('res.country', string='Country of Origin',
        help="Apply only if delivery country matches.")
    product_code = fields.Char(string='Product Code')
    tti = fields.Integer(string='TTI')
    incoterm = fields.Many2one(
        'account.incoterms', 'Incoterm',
        help="International Commercial Terms are a series of predefined commercial terms used in international transactions.")

    hs_code_id = fields.Many2one('scm.hscode', string='HS Code')


class ProductCategory(models.Model):

    _inherit = ['product.category']


    sub_business = fields.Many2one('product.category', string='Sub Business', help='For example: Modelez')
    brand = fields.Many2one('product.category', string='Brand',help='For example: Tang, cadbury')
    category = fields.Many2one('product.category', string='Category',help='For example: Silk')
    