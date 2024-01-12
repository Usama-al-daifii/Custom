from odoo import models, fields, api, _


class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'

    name = fields.Char(string='Name', required=True, trim=False)
    active = fields.Boolean(string='Active', default=True, copy=False)
    color = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")
    sequence = fields.Integer(string="Sequence")

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = dict(default or {})
        if 'name' not in default:
            default['name'] = _("%s(copy)", self.name)
        return super(PatientTag, self).copy(default)

    _sql_constraints = [
        ('unique_tag_name', 'unique(name , active)', 'Name Must Be Unique'),
        ('check_sequence', 'check(sequence > 0)', 'Sequence Must be non zero ')
    ]
