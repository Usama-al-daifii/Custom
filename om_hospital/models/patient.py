from odoo import models, fields, api, _
from datetime import date
from dateutil import relativedelta
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'  # table name ---->  'hospital_patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Patient'

    name = fields.Char(string='Name', tracking=True)
    # seq = fields.Char(string="Sequence" )
    ref = fields.Char(string="Reference", default='Odoo Mates')
    date_of_birth = fields.Date(string="Date Of Birth")
    age = fields.Integer(string='Age', compute="_compute_age", inverse="_inverse_compute_age", tracking=True,
                         search='_search_age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              String='Gender', tracking=True, default='male')
    state = fields.Selection([('new', 'New'), ('old', 'Old')],
                             string='Patient State', default='new')
    active = fields.Boolean(string="Active ", default=True)
    appointment_id = fields.Many2one(comodel_name='hospital.appointment', string='Appointment')
    image = fields.Image(string='Image')
    tag_ids = fields.Many2many(comodel_name='patient.tag', string='Tags')
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count', store=False)
    appointment_ids = fields.One2many('hospital.appointment',
                                      'patient_id', string='Appointments')
    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')],
                                      string='Marital Status')
    partner_name = fields.Char(string='Partner Name')
    is_birthday = fields.Boolean(string='Birthday ?', compute='_compute_is_birthday')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    website = fields.Char(string='Website')

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        print('----------------', self)
        # print('1111111111111111111111111111111111111')
        # count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
        appointment_group = self.env['hospital.appointment'].read_group(
            domain=[('state', 'in', ('draft', 'in_consultation', 'cancel', 'done'))],
            fields=['patient_id'], groupby=['patient_id']
        )
        for appointment in appointment_group:
            # print('appointment_group...........', appointment)
            patient_id = appointment.get('patient_id')[0]
            print('----------', patient_id)
            patient_rec = self.browse(patient_id)
            patient_rec.appointment_count = appointment['patient_id_count']
            self -= patient_rec
        self.appointment_count = 0

    @api.depends("date_of_birth")
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    @api.depends("age")
    def _inverse_compute_age(self):
        for rec in self:
            today = date.today()
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

    def _search_age(self, operator, value):
        today = date.today()
        birth_date = today - relativedelta.relativedelta(years=value)
        # print('value>>>>>>>>>>>>>', today)
        # print('value>>>>>>>>>>>>>', birth_date)
        return [('date_of_birth', '=', birth_date)]

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(f'{rec.date_of_birth} dose not come yet !')

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(f'You Can Not Delete The Patient Which have Appointments !')

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')

        res = super(HospitalPatient, self).create(vals)
        return res

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)

    def name_get(self):
        # pat_list = []
        # for rec in self:
        #     name = rec.ref + ':' + rec.name
        #     pat_list.append((rec.id, name))
        # return pat_list
        return [(rec.id, "[%s]  %s" % (rec.ref, rec.name)) for rec in self]

    def action_test(self):  # comming from appoinment_view (group by button)
        print('Clicked!!!!!!!!!!!!!!!!!!!!!')
        return

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                # print('today', today.day)
                # print('rec.date_of_birth.day', rec.date_of_birth.day)
                # print('rec.date_of_birth.month', rec.date_of_birth.month)
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday

    def action_view_appointments(self):
        return {
            'name': _('Appointments'),
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form,calendar,activity',
            'context': {'default_patient_id': self.id},
            'domain': [('patient_id', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',
        }
