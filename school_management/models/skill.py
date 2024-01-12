from odoo import models, fields, api


class Skill(models.Model):
    _name = 'iti.skill'

    name = fields.Char()
    student_ids = fields.Many2many(comodel_name="iti.student" )
