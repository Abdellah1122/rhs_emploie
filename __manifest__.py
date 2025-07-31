{
    "name": "RHS Emploi",
    "version": "1.0.0",
    "summary": "Extensions and customizations on top of hr_recruitment",
    "category": "Human Resources",
    "author": "Jorf Abdellah / Jorf Khalid",
    "license": "LGPL-3",
    "depends": [
        "hr_recruitment",
        "mail"
    ],
    "data": [
        'data/mail_templates.xml',
        "views/hr_job_views.xml",
        "views/hr_applicant_extension_views.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False
}