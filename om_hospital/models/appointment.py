from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import random


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'
    _rec_name = "seq"
    _order = "id desc"

    prescription = fields.Html(string="prescription")
    patient_id = fields.Many2one(comodel_name='hospital.patient', string='Patient', ondelete='cascade')
    gender = fields.Selection(String='Gender', related='patient_id.gender')
    ref = fields.Char(string="Reference", help="Reference of the patient from patient record")
    seq = fields.Char(string="sequence", default="New")

    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now())
    booking_date = fields.Date(string='Booking Date', default=fields.Date.today())
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High'),
        ('4', 'Perfect')], string="Priority")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string="Status", default="draft", required=True)

    doctor_id = fields.Many2one(comodel_name='res.users', string='Doctor', tracking=True, required=False)
    pharmacy_line_ids = fields.One2many(comodel_name="appointment.pharmacy.lines", inverse_name="appointment_id",
                                        string="Pharmacy Lines")
    hide_sales_price = fields.Boolean(string='Hide Sales Price')
    operation_id = fields.Many2one('hospital.operation', string='Operation')
    progress = fields.Integer(string='Progress', compute='_compute_progress')
    duration = fields.Float(string="Duration")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', 'Currency', related="company_id.currency_id")

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'
            elif rec.state == 'in_consultation':
                raise ValidationError(f'{self.patient_id.name} appointment is already In Consultation')
            else:
                raise ValidationError(f'{self.patient_id.name} appointment is Done')

    def action_done(self):
        for rec in self:
            if rec.state == 'in_consultation':
                rec.state = 'done'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Done Successfully.',
                'type': 'rainbow_man',
            }
        }

        # elif rec.state == 'done':
        #     raise ValidationError(f'{self.patient_id.name} appointment is already Done')
        # else:
        #     raise ValidationError(f'Make {self.patient_id.name} appointment In Consultation first ')

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.model
    def create(self, vals):
        vals['seq'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        res = super(HospitalAppointment, self).create(vals)
        return res

    # def write(self, vals):
    #     vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
    #     res = super(HospitalAppointment, self).create(vals)
    #     return res

    def unlink(self):
        print('1111111.............')
        for rec in self:
            if rec.state != "draft":
                raise ValidationError(
                    f"Not Allowed to delete this appointment _{rec.ref}_ which with state {rec.state} !")
        return super(HospitalAppointment, self).unlink()

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_share_whatsapp(self):
        if not self.patient_id.phone:
            raise ValidationError(f'{self.patient_id.name} did not leave his mobile phone')
        massage = f'Hi *{self.patient_id.name}*...! Your Appointment Number is *{self.seq}*'
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.patient_id.phone, massage)
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url
        }

    def action_notification(self):
        # msg = "Button Click successfully ..........."
        action = self.env.ref('om_hospital.action_hospital_patient')
        # print('**************************', action)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('click to open patient record'),
                'message': '%s',
                'links': [{
                    'label': self.patient_id.name,
                    'url': f'#action={action.id}&id={self.patient_id.id}&model=hospital.patient'
                }],
                'sticky': False,
            }
        }

    def action_test(self):
        # url action
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://surahquran.com/',
        }

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = random.randrange(0, 25)
            elif rec.state == 'in_consultation':
                progress = random.randrange(25, 99)
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress


class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _description = 'Appointment Pharmacy Lines'

    product_id = fields.Many2one(comodel_name='product.product', required=True)
    price_unit = fields.Float(string="Price", related='product_id.list_price', digits='Product Price')
    qty = fields.Integer(string="Quantity", default='1')
    appointment_id = fields.Many2one(comodel_name="hospital.appointment", string="Appointment")
    company_currency_id = fields.Many2one('res.currency', related="appointment_id.currency_id")
    price_subtotal = fields.Monetary(string="Subtotal", compute="_compute_price_subtotal",
                                     currency_field="company_currency_id")

    @api.depends('price_unit', 'qty')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.qty
