from odoo import api, fields, exceptions, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
import datetime
import logging
logger = logging.getLogger("Your Message")


class PoPartner(models.Model):
    _inherit = ['res.partner']

    vendor_code = fields.Char('Supplier Short Code', help='This code is used in po reference as a vendor short code')