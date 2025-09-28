"""
Tests for hospital stamp generator
"""

import pytest
import io
from PIL import Image
from app.modules.stamp_generator import HospitalStampGenerator


class TestHospitalStampGenerator:
    """Test cases for HospitalStampGenerator"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.generator = HospitalStampGenerator()
    
    def test_generate_stamp_basic(self):
        """Test basic stamp generation"""
        hospital_name = "City General Hospital"
        stamp_bytes = self.generator.generate_stamp(hospital_name)
        
        # Verify we got bytes
        assert isinstance(stamp_bytes, bytes)
        assert len(stamp_bytes) > 0
        
        # Verify it's a valid PNG
        image = Image.open(io.BytesIO(stamp_bytes))
        assert image.format == 'PNG'
        assert image.mode == 'RGBA'  # Should have alpha channel for transparency
    
    def test_generate_stamp_custom_size(self):
        """Test stamp generation with custom size"""
        hospital_name = "Test Hospital"
        custom_size = 400
        stamp_bytes = self.generator.generate_stamp(hospital_name, size=custom_size)
        
        # Verify image dimensions
        image = Image.open(io.BytesIO(stamp_bytes))
        assert image.size == (custom_size, custom_size)
    
    def test_generate_stamp_long_name(self):
        """Test stamp generation with long hospital name"""
        hospital_name = "Very Long Hospital Name That Should Still Work"
        stamp_bytes = self.generator.generate_stamp(hospital_name)
        
        # Should still generate successfully
        assert isinstance(stamp_bytes, bytes)
        assert len(stamp_bytes) > 0
    
    def test_generate_stamp_short_name(self):
        """Test stamp generation with short hospital name"""
        hospital_name = "Med"
        stamp_bytes = self.generator.generate_stamp(hospital_name)
        
        # Should still generate successfully
        assert isinstance(stamp_bytes, bytes)
        assert len(stamp_bytes) > 0
    
    def test_save_stamp(self, tmp_path):
        """Test saving stamp to file"""
        hospital_name = "Test Hospital"
        filename = tmp_path / "test_stamp.png"
        
        result_path = self.generator.save_stamp(hospital_name, str(filename))
        
        # Verify file was created
        assert filename.exists()
        assert result_path == str(filename)
        
        # Verify it's a valid image
        image = Image.open(filename)
        assert image.format == 'PNG'
    
    def test_calculate_font_size(self):
        """Test font size calculation"""
        # Short name should get larger font
        short_size = self.generator._calculate_font_size("Short", 300)
        
        # Long name should get smaller font
        long_size = self.generator._calculate_font_size("Very Long Hospital Name", 300)
        
        assert short_size > long_size
        assert long_size >= 8  # Minimum font size
    
    def test_transparent_background(self):
        """Test that generated stamp has transparent background"""
        hospital_name = "Test Hospital"
        stamp_bytes = self.generator.generate_stamp(hospital_name)
        
        image = Image.open(io.BytesIO(stamp_bytes))
        
        # Check corner pixels for transparency
        corner_pixel = image.getpixel((0, 0))
        assert len(corner_pixel) == 4  # RGBA
        assert corner_pixel[3] == 0  # Alpha should be 0 (transparent)