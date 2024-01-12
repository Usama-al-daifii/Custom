from odoo import api, models, fields, _


class HospitalOperation(models.Model):
    _name = 'hospital.operation'
    _description = 'Hospital Operation'
    _log_access = False
    _order = 'sequence,id'

    doctor_id = fields.Many2one(comodel_name='res.users', string='Doctor')
    operation_name = fields.Char(string='Name')
    reference_record = fields.Reference([('hospital.patient', 'Patient'),
                                         ('hospital.appointment', 'Appointment')], string='Record')
    patient_id = fields.Many2one(comodel_name='hospital.patient', string='Patient')
    sequence = fields.Integer(string="Sequence", default=10)
    # name_Create function (use it when my model Have not [name field] And [_rec_name attribute])
    @api.model
    def name_create(self, name):
        # print("0000000000000..........", name)
        return self.create({'operation_name': name}).name_get()[0]
