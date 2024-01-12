from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cancel_day = fields.Integer(string='Cancel Days', config_parameter='om_hospital.cancel_day')
