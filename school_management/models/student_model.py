from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class StudentModel(models.Model):
    _name = "iti.student"
    _rec_name = "name"  # record name by default

    name = fields.Char(required=True)
    mail = fields.Char()
    age = fields.Integer()
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ])
    info = fields.Text()
    salary = fields.Float()
    date_of_birth = fields.Date()
    interview_time = fields.Datetime()
    description = fields.Html()
    is_accepted = fields.Boolean()
    track_id = fields.Many2one(comodel_name='iti.track')
    branch = fields.Char(related='track_id.branch')
    skills_ids = fields.Many2many(comodel_name="iti.skill", relation='student_skill_relation')
    state = fields.Selection([
        ('new', 'New'),
        ('interviewing', 'Interviewing'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default="new")
    computed_age = fields.Integer(compute='compute_student_age')
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'that name already exists') ,
        ('check_salary', 'CHECK(salary > 0)', 'Salary must be greater than zero')
    ]

    @api.depends('date_of_birth')
    def compute_student_age(self):
        for record in self:
            if record.date_of_birth:
                record.computed_age = datetime.now().year - record.date_of_birth.year
            else:
                record.computed_age = 0

    @api.onchange('date_of_birth')  # decorator
    def _onchange_date_of_birth(self):
        if self.date_of_birth:
            self.age = datetime.now().year - self.date_of_birth.year
            return {
                'warning': {
                    'title': "Age Change ",
                    'message': "Age has been Changed"
                }
            }

    def set_to_interviewing(self):
        self.state = 'interviewing'

    def set_to_accepted(self):
        self.state = 'accepted'

    def set_to_rejected(self):
        self.state = 'rejected'

    # @api.constrains('mail')
    # def check_email_address(self):
    #     for record in self:
    #         if '@' not in record.mail:
    #             raise ValidationError('please insert a valid email must have "@"')

    @api.model
    def create(self, vals):
        print(vals)
        if '@' not in vals['mail']:
            vals['mail'] += '@gmail.com'
        return super().create(vals)

    def write(self, vals):
        if vals.get('mail') and '@' not in vals['mail']:
            vals['mail'] += '@gmail.com'
            return super().write(vals)
