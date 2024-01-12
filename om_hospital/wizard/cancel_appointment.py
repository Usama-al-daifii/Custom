from odoo import models, fields, api, _
import datetime
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment Wizard'

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['reason'] = ' '
        res['date_cancel'] = datetime.date.today()
        # print('1111111....', self.env.context)
        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one(comodel_name='hospital.appointment', string='Appointment')
    # domain=[('state', '=', 'draft'), ('priority', 'in', ('0', '1', False))])
    reason = fields.Text(string='Cancel Reason')
    date_cancel = fields.Date(string='Cancellation Date')

    def action_cancel(self):
        cancel_day = self.env['ir.config_parameter'].get_param('om_hospital.cancel_day')
        # print('Cancel day....', cancel_day)
        allowed_day = self.appointment_id.booking_date - relativedelta.relativedelta(days=int(cancel_day))
        # print('Cancel day....', allowed_day)
        # print('Cancel day....', relativedelta.relativedelta(days=int(cancel_day)))
        if cancel_day != 0 and allowed_day < date.today():
            raise ValidationError(_(f"Sorry, Cancellation is not allowed for this booking ! "))
        self.appointment_id.state = 'cancel'
        # to prevent closing wizard
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'cancel.appointment.wizard',
            'target': 'new',
            'res_id': self.id
        }
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload'
        # }
