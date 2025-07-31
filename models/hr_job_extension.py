# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date

class HrJob(models.Model):
    _inherit = "hr.job"

    request_date = fields.Date(
        string=_("Date de demande du poste"),
        help=_("Date à laquelle le client a demandé le poste"),
        tracking=True,
    )
    deadline_date = fields.Date(
        string=_("Date d'échéance"),
        help=_("Date limite pour pourvoir ce poste"),
        tracking=True,
    )
    nbr_jours_restants = fields.Integer(
        string=_("Jours restants"),
        compute="_compute_nbr_jours_restants",
        store=True,
        help=_("Nombre de jours restants avant la date limite"),
    )

    experience = fields.Selection(
        [
            ("0",      "Débutant (0 an)"),
            ("1_3",    "1 à 3 ans"),
            ("3_5",    "3 à 5 ans"),
            ("5_plus", "Plus de 5 ans"),
        ],
        string=_("Expérience"),
        help=_("Niveau d'expérience requis"),
        default="0",
        tracking=True,
    )
    language = fields.Selection(
        [
            ("ar", "Arabe"),
            ("fr", "Français"),
            ("en", "Anglais"),
            ("es", "Espagnol"),
            ("it", "Italien"),
            ("zh", "Chinois"),
        ],
        string=_("Langue"),
        help=_("Langue requise"),
        default="fr",
        tracking=True,
    )
    city = fields.Selection(
        [
            ("casablanca",  "Casablanca"),
            ("kenitra",     "Kénitra"),
            ("rabat",       "Rabat"),
            ("sale",        "Salé"),
            ("tanger",      "Tanger"),
            ("marrakech",   "Marrakech"),
            ("sidi_yahya",  "Sidi Yahya"),
            ("had_soualem", "Had Soualem"),
        ],
        string=_("Ville"),
        help=_("Ville(s) ciblée(s)"),
        default="casablanca",
        tracking=True,
    )
    activity_domain = fields.Selection(
        [
            ("aeronautique",       "Aéronautique"),
            ("automobile",         "Automobile"),
            ("ressources_humaines","Ressources Humaines"),
            ("industrie",          "Industrie"),
            ("agroalimentaire",    "Agroalimentaire"),
            ("archivage",          "Archivage / Documentation"),
            ("pharmaceutique",     "Pharmaceutique"),
            ("btp",                "BTP & Génie Civil"),
            ("immobilier",         "Immobilier"),
            ("commerce",           "Commerce & Distribution"),
            ("juridique",          "Services Juridiques & Conseil"),
            ("comptabilite",       "Comptabilité"),
            ("logistique",         "Logistique / Transport"),
            ("achat",              "Achat"),
            ("informatique",       "Informatique"),
            ("finance",            "Finance"),
            ("maintenance",        "Maintenance"),
            ("qualite",            "Qualité"),
            ("comptable",          "Comptable"),
            ("autre",              "Autre (à préciser)"),
        ],
        string=_("Domaine d'activité"),
        help=_("Secteur métier du poste"),
        default="autre",
        tracking=True,
    )
    status = fields.Selection(
        [
            ("ouvert",        "Ouvert"),
            ("non_commencee", "Non commencée"),
            ("en_cours",      "En cours"),
            ("annule",        "Annulé"),
            ("cloture",       "Clôturé"),
            ("gele",          "Gelé"),
        ],
        string=_("Statut du suivi"),
        help=_("État d'avancement du recrutement"),
        default="ouvert",
        tracking=True,
    )
    
    # Fixed contract type field
    type_contrat = fields.Selection([
        ("interim", "Travail temporaire (Intérim)"),
        ("cdd", "CDD"),
        ("cdi", "CDI"),
        ("stage", "Stage"),
        ("freelance", "Freelance"),
    ], 
    string=_("Type de contrat"),
    help=_("Type de contrat proposé pour ce poste"),
    tracking=True,
    )
    
    # Fixed document fields with proper names and conditional visibility
    copy_cin = fields.Boolean(
        string="2 copies CIN légalisées",
        help="Document requis pour le recrutement"
    )
    doc_rib = fields.Boolean(
        string="RIB bancaire",
        help="Document requis pour le recrutement"
    )
    doc_cv = fields.Boolean(
        string="CV",
        help="Document requis pour le recrutement"
    )
    doc_cnss = fields.Boolean(
        string="Affiliation à la CNSS",
        help="Document requis pour le recrutement"
    )
    doc_diplomes = fields.Boolean(
        string="Copie des diplômes et/ou certificats",
        help="Document requis pour le recrutement"
    )
    doc_attestations = fields.Boolean(
        string="Attestations de stage et/ou de travail",
        help="Document requis pour le recrutement"
    )
    doc_photos = fields.Boolean(
        string="4 Photos d'identité récentes",
        help="Document requis pour le recrutement"
    )
    doc_anthropometrique = fields.Boolean(
        string="Fiche anthropométrique",
        help="Document requis pour le recrutement"
    )
    doc_aptitude = fields.Boolean(
        string="Fiche d'aptitude",
        help="Document requis pour le recrutement"
    )
    doc_radiologie = fields.Boolean(
        string="Radiologie pulmonaire",
        help="Document requis pour le recrutement"
    )
    
    # Additional useful fields
    documents_required_interim = fields.Text(
        string="Documents requis (Intérim)",
        help="Liste des documents spécifiques requis pour les postes d'intérim",
        compute="_compute_documents_required_interim",
        store=False
    )
    
    # === COMPUTE FIELDS ===
    @api.depends('deadline_date')
    def _compute_nbr_jours_restants(self):
        """Compute remaining days until deadline with enhanced logic"""
        for job in self:
            if job.deadline_date:
                today = date.today()
                delta = (job.deadline_date - today).days
                job.nbr_jours_restants = delta
            else:
                job.nbr_jours_restants = 0

    @api.depends('type_contrat', 'copy_cin', 'doc_rib', 'doc_cv', 'doc_cnss', 'doc_diplomes', 
                 'doc_attestations', 'doc_photos', 'doc_anthropometrique', 'doc_aptitude', 'doc_radiologie')
    def _compute_documents_required_interim(self):
        """Compute list of required documents for interim positions"""
        for job in self:
            if job.type_contrat == 'interim':
                docs = []
                if job.copy_cin:
                    docs.append("• 2 copies CIN légalisées")
                if job.doc_rib:
                    docs.append("• RIB bancaire")
                if job.doc_cv:
                    docs.append("• CV")
                if job.doc_cnss:
                    docs.append("• Affiliation à la CNSS")
                if job.doc_diplomes:
                    docs.append("• Copie des diplômes et/ou certificats")
                if job.doc_attestations:
                    docs.append("• Attestations de stage et/ou de travail")
                if job.doc_photos:
                    docs.append("• 4 Photos d'identité récentes")
                if job.doc_anthropometrique:
                    docs.append("• Fiche anthropométrique")
                if job.doc_aptitude:
                    docs.append("• Fiche d'aptitude")
                if job.doc_radiologie:
                    docs.append("• Radiologie pulmonaire")
                
                job.documents_required_interim = "\n".join(docs) if docs else "Aucun document spécifique requis"
            else:
                job.documents_required_interim = ""

    # === CONSTRAINTS ===
    @api.constrains('request_date', 'deadline_date')
    def _check_dates(self):
        """Enhanced date validation with better error messages"""
        for job in self:
            if job.request_date and job.deadline_date:
                if job.deadline_date < job.request_date:
                    raise ValidationError(_(
                        "La date d'échéance (%s) ne peut pas être antérieure à la date de demande (%s) "
                        "pour le poste '%s'."
                    ) % (job.deadline_date, job.request_date, job.name))
                
                # Allow past deadlines but show warning in kanban through days remaining
                # This is more flexible for real-world scenarios
    
    # === ONCHANGE METHODS ===
    @api.onchange('type_contrat')
    def _onchange_type_contrat(self):
        """Set default document requirements when contract type changes"""
        if self.type_contrat == 'interim':
            # Set default documents for interim positions
            self.copy_cin = True
            self.doc_rib = True
            self.doc_cv = True
            self.doc_cnss = True
            self.doc_diplomes = True
            self.doc_attestations = True
            self.doc_photos = True
            self.doc_anthropometrique = True
            self.doc_aptitude = True
            self.doc_radiologie = True
        else:
            # Clear document requirements for other contract types
            self.copy_cin = False
            self.doc_rib = False
            self.doc_cv = False
            self.doc_cnss = False
            self.doc_diplomes = False
            self.doc_attestations = False
            self.doc_photos = False
            self.doc_anthropometrique = False
            self.doc_aptitude = False
            self.doc_radiologie = False
    
    # === UTILITY METHODS ===
    def get_status_color(self):
        """Return color class for status display"""
        status_colors = {
            'ouvert': 'success',
            'en_cours': 'warning', 
            'cloture': 'secondary',
            'annule': 'danger',
            'non_commencee': 'info',
            'gele': 'dark'
        }
        return status_colors.get(self.status, 'primary')
    
    def get_urgency_level(self):
        """Return urgency level based on remaining days"""
        if self.nbr_jours_restants < 0:
            return 'overdue'
        elif self.nbr_jours_restants <= 7:
            return 'urgent'
        elif self.nbr_jours_restants <= 30:
            return 'warning'
        else:
            return 'normal'
    
    def get_required_documents_list(self):
        """Get list of required documents for this job"""
        documents = []
        doc_mapping = {
            'copy_cin': '2 copies CIN légalisées',
            'doc_rib': 'RIB bancaire',
            'doc_cv': 'CV',
            'doc_cnss': 'Affiliation à la CNSS',
            'doc_diplomes': 'Copie des diplômes et/ou certificats',
            'doc_attestations': 'Attestations de stage et/ou de travail',
            'doc_photos': '4 Photos d\'identité récentes',
            'doc_anthropometrique': 'Fiche anthropométrique',
            'doc_aptitude': 'Fiche d\'aptitude',
            'doc_radiologie': 'Radiologie pulmonaire'
        }
        
        for field, label in doc_mapping.items():
            if getattr(self, field, False):
                documents.append(label)
        
        return documents
    
    @api.model
    def get_status_statistics(self):
        """Get statistics for dashboard/reporting"""
        domain = [('active', '=', True)]
        total = self.search_count(domain)
        
        stats = {}
        for status, label in self._fields['status'].selection:
            count = self.search_count(domain + [('status', '=', status)])
            stats[status] = {
                'count': count,
                'percentage': round((count / total * 100) if total else 0, 1),
                'label': label
            }
        
        return {
            'total': total,
            'by_status': stats,
            'urgent_count': self.search_count(domain + [('nbr_jours_restants', '<=', 7)]),
            'overdue_count': self.search_count(domain + [('nbr_jours_restants', '<', 0)])
        }