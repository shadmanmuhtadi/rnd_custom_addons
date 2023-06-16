# -*- coding: utf-8 -*-

import math
import logging
from datetime import timedelta
from itertools import repeat

import pytz

from odoo import api, fields, models, Command
from odoo.osv.expression import AND
from odoo.addons.base.models.res_partner import _tz_get
from odoo.addons.calendar.models.calendar_attendee import Attendee
from odoo.addons.calendar.models.calendar_recurrence import (
    weekday_to_field,
    RRULE_TYPE_SELECTION,
    END_TYPE_SELECTION,
    MONTH_BY_SELECTION,
    WEEKDAY_SELECTION,
    BYDAY_SELECTION
)
from odoo.tools.translate import _
from odoo.tools.misc import get_lang
from odoo.tools import pycompat, html2plaintext, is_html_empty
from odoo.exceptions import UserError, ValidationError

class PersonalInfo(models.Model):
    _inherit = "calendar.event"


    room_id = fields.Many2one('meeting.room',string='Meeting Room',help="Location of Event",ondelete='cascade',required=True)
    location = fields.Char('Location',compute='get_location', tracking=True, help="Location of Event")
    calendar_event_type = fields.Char(string='Event Type')


    #to check weather a room and schedule is available or not
    @api.constrains('start', 'stop', 'room_id','calendar_event_type')
    def check_meeting_conflict(self):
        for meeting in self:
            if meeting.calendar_event_type ==  'event_type_meeting':
                domain = [
                    ('room_id', '=', meeting.room_id.id),
                    ('start', '<', meeting.stop),
                    ('stop', '>', meeting.start),
                    ('id', '!=', meeting.id)
                ]
                conflicting_meetings = self.search(domain)
                if conflicting_meetings:
                    raise ValidationError('This room is already booked for the selected time range. Please select a different room or time range.')
  
    #to auto fill up the location
    @api.depends('room_id')
    def get_location(self):
        for rec in self:
            rec.location = rec.room_id.name

    #to auto fill up the calendar_event_type
    @api.onchange('room_id')
    def onchange_room_id(self):
        if self.room_id:
            self.calendar_event_type = 'event_type_meeting'
        else:
            self.calendar_event_type = False

class MeetingRoom(models.Model):
    _name = 'meeting.room'
    _description = "Meeting Room"
    _rec_name = 'name'


    name = fields.Char(string="Room Name")
    capacity = fields.Integer(string="Room Capacity",help="Number of sitting arrangement")
    description = fields.Html('Description')
    image = fields.Image(string="Image")
