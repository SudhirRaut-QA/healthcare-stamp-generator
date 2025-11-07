# -*- coding: utf-8 -*-

"""
Hospital Stamp Generator Adapter for Odoo Integration

This module provides a bridge between Odoo models and the core
hospital stamp generation functionality.
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
    from modules.stamp_generator.generator import HospitalStampGenerator
except ImportError:
    # Fallback if core generator not available
    HospitalStampGenerator = None

class HospitalStampAdapter:
    """
    Adapter class to bridge Odoo hospital stamp model with core generator.
    
    This class handles the conversion between Odoo model data and the
    parameters expected by the core hospital stamp generator.
    """
    
    def __init__(self):
        """Initialize the adapter."""
        self.generator = HospitalStampGenerator() if HospitalStampGenerator else None
    
    def is_available(self):
        """Check if the core generator is available."""
        return self.generator is not None

    
    def generate_stamp(self, hospital_name, size=300, **kwargs):
        """
        Generate hospital stamp using core generator.
        
        Args:
            hospital_name (str): Name of the hospital
            size (int): Size of the stamp in pixels (default: 300)
            **kwargs: Additional parameters
            
        Returns:
            tuple: (success, image_base64, error_message)
        """
        if not self.is_available():
            return False, None, "Core hospital stamp generator not available"
        
        try:
            # Generate stamp using core generator
            # Note: The core generator returns PNG bytes directly, not a PIL Image
            stamp_bytes = self.generator.generate_stamp(
                hospital_name=hospital_name,
                size=size,
                **kwargs
            )
            
            # The core generator returns bytes directly, convert to base64 for Odoo storage
            if isinstance(stamp_bytes, bytes):
                image_base64 = base64.b64encode(stamp_bytes).decode('utf-8')
                return True, image_base64, None
            else:
                return False, None, "Generator returned invalid data type"
            
        except Exception as e:
            return False, None, str(e)
    
    def validate_parameters(self, hospital_name, size=300):
        """
        Validate stamp generation parameters.
        
        Args:
            hospital_name (str): Name of the hospital
            size (int): Size of the stamp
            
        Returns:
            tuple: (valid, error_message)
        """
        if not hospital_name or not hospital_name.strip():
            return False, "Hospital name is required"
        
        if len(hospital_name.strip()) > 50:
            return False, "Hospital name too long (max 50 characters)"
        
        if not isinstance(size, int) or size < 180 or size > 500:
            return False, "Size must be between 180 and 500 pixels"
        
        return True, None
    
    def get_stamp_filename(self, hospital_name, size=300):
        """
        Generate appropriate filename for the stamp.
        
        Args:
            hospital_name (str): Name of the hospital
            size (int): Size of the stamp
            
        Returns:
            str: Suggested filename
        """
        # Clean hospital name for filename
        clean_name = "".join(c for c in hospital_name if c.isalnum() or c in (' ', '-', '_')).strip()
        clean_name = clean_name.replace(' ', '_')
        
        return f"hospital_stamp_{clean_name}_{size}px.png"
    
    def get_default_parameters(self):
        """
        Get default parameters for hospital stamp generation.
        
        Returns:
            dict: Default parameters
        """
        return {
            'size': 300,
            'outer_radius_ratio': 0.45,
            'inner_radius_ratio': 0.32,
            'font_color': '#1E40AF',
            'background_color': 'transparent'
        }
    
    def get_size_recommendations(self):
        """
        Get size recommendations for different use cases.
        
        Returns:
            dict: Size recommendations
        """
        return {
            'small': {'size': 180, 'use_case': 'Small documents, letterheads'},
            'medium': {'size': 300, 'use_case': 'Standard documents, certificates'},
            'large': {'size': 400, 'use_case': 'Large documents, posters'},
            'extra_large': {'size': 500, 'use_case': 'High-resolution printing'}
        }
