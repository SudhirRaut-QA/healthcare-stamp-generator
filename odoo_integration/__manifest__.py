{
    'name': 'Healthcare Stamp Generator',
    'version': '1.0.0',
    'category': 'Healthcare',
    'summary': 'Generate professional hospital and doctor stamps for healthcare operations',
    'description': """
        Healthcare Stamp Generator
        =========================
        
        This module provides comprehensive stamp generation capabilities for healthcare facilities:
        
        Features:
        ---------
        * Hospital Stamps: Circular design with dynamic spacing and dual padding
        * Doctor Stamps: Rectangular layout with realistic fonts and bright colors
        * Integration with Odoo models (Partners, Employees)
        * Professional medical appearance
        * Transparent PNG output for easy integration
        * RESTful API for external systems
        * Batch generation capabilities
        * Report integration
        
        Perfect for:
        -----------
        * Hospitals and Medical Centers
        * Healthcare Management Systems
        * Medical Documentation
        * Professional Medical Reports
        * Patient Records and Prescriptions
    """,
    'author': 'Healthcare Solutions',
    'website': 'https://github.com/SudhirRaut-QA/healthcare-stamp-generator',
    'license': 'MIT',
    'depends': ['base', 'hr', 'mail'],
    'external_dependencies': {
        'python': ['PIL', 'requests'],
    },
    'data': [
        'security/ir.model.access.csv',
        'data/demo_data.xml',
        'views/menu_views.xml',
        'views/hospital_stamp_views.xml',
        'views/doctor_stamp_views.xml',
        'wizard/stamp_wizard_views.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'qweb': [
        'static/src/xml/stamp_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 10,
    'images': ['static/description/icon.png'],
}