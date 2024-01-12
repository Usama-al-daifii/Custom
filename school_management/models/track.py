from odoo import models, fields, api


class Track(models.Model):
    _name = 'iti.track'
    _description = 'Track'

    name = fields.Char(string=" Title ", required=True)
    branch = fields.Char()
    info = fields.Text(string=" info ")
    description = fields.Html()
    capacity = fields.Integer()
    start_date = fields.Date()
    is_open = fields.Boolean()
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    student_ids = fields.One2many(comodel_name='iti.student',inverse_name='track_id')
    # take table and  relation itself
    ###one2many Attributtes  -->    comodel_name = " table_name " #inverse_name=" many2one field "