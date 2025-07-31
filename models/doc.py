# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date

class Document(models.Model):
   _name="rhs.docs"
   _description="Documents"

   nom=fields.Char(string="Nom du Document")
   doc=fields.Binary(string="Document")
   candidature_id = fields.Many2one('hr.applicant', string="Candidature", required=True)
   type_doc=fields.Selection([
      ("guide","Guide d'entretien"),
      ("guidet","Guide Telephonique"),
   ])


