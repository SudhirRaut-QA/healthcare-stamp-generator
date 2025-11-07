# -*- coding: utf-8 -*-

"""
Doctor Stamp Generator Adapter for Odoo Integration

This module provides a bridge between Odoo models and the core  
doctor stamp generation functionality.
"""

import os
import sys
import base64
from io import BytesIO

# Add the main app directory to Python path to import core generators
# IMPORTANT: Update this path to your actual project location
# For production: Use absolute path to your healthcare-stamp-generator/app directory
# Example: app_path = '/opt/healthcare-stamp-generator/app'
app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'app')
if app_path not in sys.path:
    sys.path.append(app_path)

try:
    from modules.doctor_stamp.generator import DoctorStampGenerator
except ImportError:
    # Fallback if core generator not available
    DoctorStampGenerator = None

class DoctorStampAdapter:
    """
    Adapter class to bridge Odoo doctor stamp model with core generator.
    
    This class handles the conversion between Odoo model data and the
    parameters expected by the core doctor stamp generator.
    """
    
    def __init__(self):
        """Initialize the adapter."""
        self.generator = DoctorStampGenerator() if DoctorStampGenerator else None
    
    def is_available(self):
        """Check if the core generator is available."""
        return self.generator is not None


    
    def generate_stamp(self, name, degree="", registration_number="", width=400, height=200, **kwargs):
        """
        Generate doctor stamp using core generator.
        
        Args:
            name (str): Doctor's name
            degree (str): Doctor's degree/qualification
            registration_number (str): Registration number
            width (int): Stamp width in pixels (default: 400)
            height (int): Stamp height in pixels (default: 200)
            **kwargs: Additional parameters
            
        Returns:
            tuple: (success, image_base64, error_message)
        """
        if not self.is_available():
            return False, None, "Core doctor stamp generator not available"
        
        try:
            # Generate stamp using core generator
            # Note: The doctor stamp generator saves to file and returns the file path
            output_path = self.generator.generate_doctor_stamp(
                doctor_name=name,
                degree=degree,
                registration_number=registration_number,
                width=width,
                height=200,
                **kwargs
            )
            
            # Read the generated file and convert to base64 for Odoo storage
            if output_path and os.path.exists(output_path):
                with open(output_path, 'rb') as f:
                    stamp_bytes = f.read()
                image_base64 = base64.b64encode(stamp_bytes).decode('utf-8')
                return True, image_base64, None
            else:
                return False, None, "Generator failed to create stamp file"
            
        except Exception as e:
            return False, None, str(e)
    
    def validate_parameters(self, name, degree="", registration_number="", width=400, height=200):
        """
        Validate stamp generation parameters.
        
        Args:
            name (str): Doctor's name
            degree (str): Doctor's degree
            registration_number (str): Registration number
            width (int): Stamp width
            height (int): Stamp height
            
        Returns:
            tuple: (valid, error_message)
        """
        if not name or not name.strip():
            return False, "Doctor name is required"
        
        if len(name.strip()) > 40:
            return False, "Doctor name too long (max 40 characters)"
        
        if degree and len(degree) > 60:
            return False, "Degree too long (max 60 characters)"
        
        if registration_number and len(registration_number) > 30:
            return False, "Registration number too long (max 30 characters)"
        
        if not isinstance(width, int) or width < 200 or width > 800:
            return False, "Width must be between 200 and 800 pixels"
            
        if not isinstance(height, int) or height < 100 or height > 400:
            return False, "Height must be between 100 and 400 pixels"
        
        return True, None
    
    def get_stamp_filename(self, name, width=400, height=200):
        """
        Generate appropriate filename for the stamp.
        
        Args:
            name (str): Doctor's name
            width (int): Stamp width
            height (int): Stamp height
            
        Returns:
            str: Suggested filename
        """
        # Clean doctor name for filename
        clean_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
        clean_name = clean_name.replace(' ', '_')
        
        return f"doctor_stamp_{clean_name}_{width}x{height}px.png"
    
    def get_default_parameters(self):
        """
        Get default parameters for doctor stamp generation.
        
        Returns:
            dict: Default parameters
        """
        return {
            'width': 400,
            'height': 200,
            'background_color': '#F8F9FA',
            'border_color': '#2F4F8F',
            'text_color': '#2F4F8F',
            'name_color': '#364F7A',
            'border_width': 3
        }
    
    def get_size_recommendations(self):
        """
        Get size recommendations for different use cases.
        
        Returns:
            dict: Size recommendations
        """
        return {
            'small': {'width': 200, 'height': 100, 'use_case': 'Prescription pads, small forms'},
            'medium': {'width': 400, 'height': 200, 'use_case': 'Standard prescriptions, certificates'},
            'large': {'width': 600, 'height': 300, 'use_case': 'Medical reports, official documents'},
            'extra_large': {'width': 800, 'height': 400, 'use_case': 'High-resolution printing, posters'}
        }
    
    def format_doctor_info(self, name, degree="", registration_number=""):
        """
        Format doctor information for display.
        
        Args:
            name (str): Doctor's name
            degree (str): Doctor's degree
            registration_number (str): Registration number
            
        Returns:
            dict: Formatted information
        """
        return {
            'display_name': f"Dr. {name}" if not name.startswith('Dr.') else name,
            'degree_text': degree.strip() if degree else "",
            'registration_text': registration_number.strip() if registration_number else "",
            'full_text': f"Dr. {name}{', ' + degree if degree else ''}{', ' + registration_number if registration_number else ''}"
        }