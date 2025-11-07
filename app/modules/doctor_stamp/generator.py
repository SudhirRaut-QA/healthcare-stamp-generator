"""
Professional Doctor Stamp Generator Module

This module generates realistic professional doctor stamps with:
- Doctor's name (largest font)
- Degree/Qualification (medium font)  
- Registration number (smaller font)
- Professional rectangular layout
- Authentic medical appearance
"""

from PIL import Image, ImageDraw, ImageFont
import os
from typing import Tuple, Optional
import textwrap


class DoctorStampGenerator:
    """Generate professional rectangular doctor stamps with authentic medical appearance."""
    
    def __init__(self):
        self.default_width = 400
        self.default_height = 200
        self.background_color = (255, 255, 255, 0)  # Transparent
        self.text_color = "#2F4F8F"  # Realistic ink blue - muted and authentic
        self.border_color = "#2F4F8F"  # Matching border color
        self.padding = 20
        
    def _get_font_path(self, size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
        """
        Get appropriate font with fallback system for authentic medical appearance.
        
        Args:
            size: Font size in pixels
            weight: Font weight ("bold", "regular", "medium")
            
        Returns:
            ImageFont.FreeTypeFont: Loaded font object
        """
        font_paths = {
            "bold": [
                # Professional medical fonts (serif for authenticity)
                "C:/Windows/Fonts/timesbd.ttf",    # Times New Roman Bold (medical standard)
                "C:/Windows/Fonts/Georgia Bold.ttf", # Georgia Bold (professional)
                "C:/Windows/Fonts/calibrib.ttf",   # Calibri Bold (modern)
                "C:/Windows/Fonts/arialbd.ttf",    # Arial Bold (fallback)
                "/System/Library/Fonts/Times.ttc", # macOS Times
                "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",  # Linux
            ],
            "medium": [
                # Semi-bold fonts for degrees
                "C:/Windows/Fonts/timesbd.ttf",    # Times Bold (used as medium)
                "C:/Windows/Fonts/Georgia Bold.ttf", # Georgia Bold
                "C:/Windows/Fonts/calibrib.ttf",   # Calibri Bold
                "C:/Windows/Fonts/arialbd.ttf",    # Arial Bold
                "/System/Library/Fonts/Times.ttc", # macOS
                "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",  # Linux
            ],
            "regular": [
                # Regular fonts for registration numbers
                "C:/Windows/Fonts/times.ttf",      # Times New Roman (medical standard)
                "C:/Windows/Fonts/georgia.ttf",    # Georgia (professional)
                "C:/Windows/Fonts/calibri.ttf",    # Calibri (modern)
                "C:/Windows/Fonts/arial.ttf",      # Arial (fallback)
                "/System/Library/Fonts/Times.ttc", # macOS
                "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",  # Linux
            ]
        }
        
        for font_path in font_paths.get(weight, font_paths["regular"]):
            try:
                return ImageFont.truetype(font_path, size)
            except (OSError, IOError):
                continue
                
        # Fallback to default font
        try:
            return ImageFont.load_default()
        except:
            return ImageFont.load_default()
    
    def _calculate_text_dimensions(self, text: str, font: ImageFont.FreeTypeFont) -> Tuple[int, int]:
        """Calculate text width and height."""
        bbox = font.getbbox(text)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    def _wrap_long_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list:
        """Wrap long text to fit within specified width."""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            text_width, _ = self._calculate_text_dimensions(test_line, font)
            
            if text_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
            
        return lines
    
    def _draw_enhanced_text(self, draw: ImageDraw.Draw, text: str, position: tuple, font: ImageFont.FreeTypeFont, is_name: bool = False):
        """
        Draw enhanced text with bright colors and subtle shadow for maximum visibility.
        
        Args:
            draw: ImageDraw object
            text: Text to draw
            position: (x, y) position
            font: Font to use
            is_name: Whether this is the doctor's name (gets extra enhancement)
        """
        x, y = position
        
        # For doctor names, add a subtle shadow for more prominence and depth
        if is_name:
            # Light shadow for depth (1px offset) in darker blue
            shadow_color = "#004080"  # Medium blue for shadow
            draw.text((x + 1, y + 1), text, fill=shadow_color, font=font)
            
            # Use even brighter color for doctor names
            name_color = "#0080FF"  # Extra bright blue for names
            draw.text((x, y), text, fill=name_color, font=font)
        else:
            # Main text in bright professional blue
            draw.text((x, y), text, fill=self.text_color, font=font)
    
    def _draw_professional_border(self, draw: ImageDraw.Draw, width: int, height: int):
        """Draw professional double border around the stamp."""
        # Outer border (thicker) - using the same realistic blue as text
        draw.rectangle([2, 2, width-3, height-3], outline=self.text_color, width=3)
        
        # Inner border (thinner) 
        draw.rectangle([8, 8, width-9, height-9], outline=self.text_color, width=1)
    
    def generate_doctor_stamp(
        self,
        doctor_name: str,
        degree: str,
        registration_number: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate professional doctor stamp with authentic medical appearance.
        
        Args:
            doctor_name: Doctor's full name (e.g., "Dr. Sarah Johnson")
            degree: Medical degree/qualification (e.g., "MBBS, MD (Cardiology)")
            registration_number: Medical registration number (e.g., "Reg. No: MCI-12345")
            width: Stamp width in pixels (default: 400)
            height: Stamp height in pixels (default: 200)  
            output_path: Custom output file path
            
        Returns:
            str: Path to generated stamp file
            
        Raises:
            ValueError: If required parameters are missing
        """
        if not doctor_name or not degree or not registration_number:
            raise ValueError("Doctor name, degree, and registration number are required")
            
        width = width or self.default_width
        height = height or self.default_height
        
        # Create image with transparent background
        image = Image.new("RGBA", (width, height), self.background_color)
        draw = ImageDraw.Draw(image)
        
        # Calculate available text area (no borders, so full width available)
        text_area_width = width - (self.padding * 2)
        text_area_height = height - (self.padding * 2)
        
        # Enhanced font sizes for better visibility and professional appearance
        name_font_size = max(28, width // 14)     # Larger doctor name
        degree_font_size = max(18, width // 22)   # Medium degree text  
        reg_font_size = max(14, width // 28)      # Larger registration text
        
        # Load fonts with proper hierarchy
        name_font = self._get_font_path(name_font_size, "bold")      # Bold for doctor name
        degree_font = self._get_font_path(degree_font_size, "medium") # Medium for degree
        reg_font = self._get_font_path(reg_font_size, "regular")     # Regular for registration
        
        # Calculate text positioning (no border offset needed)
        y_start = self.padding
        line_spacing = 8
        
        # 1. Doctor Name (Top - Bold and Largest with enhanced visibility)
        name_lines = self._wrap_long_text(doctor_name, name_font, text_area_width)
        current_y = y_start
        
        for line in name_lines:
            text_width, text_height = self._calculate_text_dimensions(line, name_font)
            x_centered = (width - text_width) // 2
            self._draw_enhanced_text(draw, line, (x_centered, current_y), name_font, is_name=True)
            current_y += text_height + line_spacing
        
        current_y += 12  # Extra space after name
        
        # 2. Degree/Qualification (Middle - Medium weight)
        degree_lines = self._wrap_long_text(degree, degree_font, text_area_width)
        
        for line in degree_lines:
            text_width, text_height = self._calculate_text_dimensions(line, degree_font)
            x_centered = (width - text_width) // 2
            self._draw_enhanced_text(draw, line, (x_centered, current_y), degree_font)
            current_y += text_height + line_spacing
            
        current_y += 10  # Extra space after degree
        
        # 3. Registration Number (Bottom - Regular with good visibility)
        # Ensure "Reg. No.:" prefix is always present
        if not registration_number.strip().lower().startswith(('reg.', 'reg ', 'registration')):
            formatted_registration = f"Reg. No.: {registration_number.strip()}"
        else:
            formatted_registration = registration_number.strip()
        
        reg_lines = self._wrap_long_text(formatted_registration, reg_font, text_area_width)
        
        for line in reg_lines:
            text_width, text_height = self._calculate_text_dimensions(line, reg_font)
            x_centered = (width - text_width) // 2
            self._draw_enhanced_text(draw, line, (x_centered, current_y), reg_font)
            current_y += text_height + line_spacing
        
        # Generate output filename if not provided
        if not output_path:
            # Create safe filename from doctor name
            safe_name = "".join(c for c in doctor_name.lower() if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            output_path = f"doctorStampOutput/doctor_stamp_{safe_name}.png"
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the stamp
        image.save(output_path, "PNG")
        
        return output_path
    
    def generate_batch_stamps(self, doctors_data: list) -> list:
        """
        Generate multiple doctor stamps from a list of doctor data.
        
        Args:
            doctors_data: List of dictionaries with keys: 'name', 'degree', 'registration'
            
        Returns:
            list: List of generated file paths
        """
        generated_files = []
        
        for doctor_data in doctors_data:
            try:
                file_path = self.generate_doctor_stamp(
                    doctor_name=doctor_data['name'],
                    degree=doctor_data['degree'], 
                    registration_number=doctor_data['registration']
                )
                generated_files.append(file_path)
            except Exception as e:
                print(f"Error generating stamp for {doctor_data.get('name', 'Unknown')}: {e}")
                
        return generated_files


def create_doctor_stamp(doctor_name: str, degree: str, registration_number: str, **kwargs) -> str:
    """
    Convenience function to create a doctor stamp.
    
    Args:
        doctor_name: Doctor's full name
        degree: Medical degree/qualification
        registration_number: Medical registration number
        **kwargs: Additional arguments (width, height, output_path)
        
    Returns:
        str: Path to generated stamp file
    """
    generator = DoctorStampGenerator()
    return generator.generate_doctor_stamp(doctor_name, degree, registration_number, **kwargs)


# Example usage and testing
if __name__ == "__main__":
    # Test the doctor stamp generator
    generator = DoctorStampGenerator()
    
    # Example doctor stamps
    examples = [
        {
            "name": "Dr. Sarah Johnson",
            "degree": "MBBS, MD (Cardiology)",
            "registration": "MCI-12345"
        },
        {
            "name": "Dr. Michael Chen",
            "degree": "MBBS, MS (Orthopedics)",
            "registration": "MCI-67890"
        },
        {
            "name": "Dr. Priya Sharma",
            "degree": "MBBS, DGO, MD (Gynecology)",
            "registration": "MCI-11223"
        }
    ]
    
    print("🩺 Testing Doctor Stamp Generator...")
    
    for example in examples:
        try:
            file_path = generator.generate_doctor_stamp(
                doctor_name=example["name"],
                degree=example["degree"],
                registration_number=example["registration"]
            )
            print(f"✅ Generated: {file_path}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("🎉 Doctor stamp generation complete!")