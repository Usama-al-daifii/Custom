from odoo import models, fields, api


class TrackWizard(models.TransientModel):
    _name = 'iti.track.wizard'

    name = fields.Char()
    description = fields.Text()

    def save_track_values(self):
        # self.env['iti.track'].create({      # env >> contain all names of models
        #     'name': self.name,
        #     'description': self.description,
        #
        # })
        students = self.env['iti.student'].search([('state', '=', 'accepted')])
        students.unlink()
        print(students)

# >>>ORM<<<
# CRUD
# create
# read --> Search
# update --> write
# delete --> unlink
#
