# -*- coding: utf-8 -*-
from odoo import fields, models

class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    etablissement = fields.Char(string="Établissement")
    address=fields.Char(string="Address du Domicile")
    date_obtention = fields.Date(string="Date d’obtention")
