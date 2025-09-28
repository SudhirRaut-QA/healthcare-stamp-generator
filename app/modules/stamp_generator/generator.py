"""
Hospital Stamp Generator Module
Generates circular hospital stamps with transparent background and blue ink
"""

from PIL import Image, ImageDraw, ImageFont
import io
import math
from typing import Optional, Tuple


class HospitalStampGenerator:
    """
    Generate circular hospital stamps with transparent background
    """
    
    def __init__(self):
        self.default_size = 300
        self.default_color = (0, 100, 200, 255)  # Blue color with alpha
        self.background_color = (255, 255, 255, 0)  # Transparent background
    
    def generate_stamp(
        self, 
        hospital_name: str, 
        size: int = 300,
        font_size: Optional[int] = None,
        color: Tuple[int, int, int, int] = (0, 100, 200, 255)
    ) -> bytes:
        """
        Generate a circular hospital stamp
        
        Args:
            hospital_name: Name of the hospital
            size: Size of the stamp (diameter in pixels)
            font_size: Font size for text (auto-calculated if None)
            color: RGBA color tuple for the stamp
            
        Returns:
            PNG image as bytes
        """
        # Create image with transparent background
        image = Image.new('RGBA', (size, size), self.background_color)
        draw = ImageDraw.Draw(image)
        
        # Calculate circle parameters
        center = size // 2
        radius = center - 10  # Leave some margin
        
        # Draw outer circle (thick border)
        border_width = 8
        for i in range(border_width):
            draw.ellipse(
                [center - radius + i, center - radius + i, 
                 center + radius - i, center + radius - i],
                outline=color,
                width=1
            )
        
        # Draw inner circle (thin border)
        inner_radius = radius - 20
        draw.ellipse(
            [center - inner_radius, center - inner_radius,
             center + inner_radius, center + inner_radius],
            outline=color,
            width=2
        )
        
        # Calculate font size if not provided
        if font_size is None:
            font_size = self._calculate_font_size(hospital_name, size)
        
        # Try to load a font, fallback to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except (OSError, IOError):
            try:
                font = ImageFont.truetype("Arial.ttf", font_size)
            except (OSError, IOError):
                font = ImageFont.load_default()
        
        # Prepare text for circular arrangement
        text_upper = hospital_name.upper()
        
        # Draw text along the circle
        self._draw_circular_text(
            draw, text_upper, center, center, inner_radius - 15, font, color
        )
        
        # Add center text (like "HOSPITAL" or medical symbol)
        center_text = "★ HOSPITAL ★"
        try:
            center_font = ImageFont.truetype("arial.ttf", font_size // 2)
        except (OSError, IOError):
            center_font = font
            
        # Get text bounding box
        bbox = draw.textbbox((0, 0), center_text, font=center_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Draw center text
        draw.text(
            (center - text_width // 2, center - text_height // 2),
            center_text,
            font=center_font,
            fill=color
        )
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG', optimize=True)
        img_byte_arr.seek(0)
        
        return img_byte_arr.getvalue()
    
    def _calculate_font_size(self, text: str, stamp_size: int) -> int:
        """Calculate appropriate font size based on text length and stamp size"""
        base_size = stamp_size // 15
        text_length = len(text)
        
        if text_length <= 15:
            return base_size
        elif text_length <= 25:
            return max(base_size - 2, 12)
        elif text_length <= 35:
            return max(base_size - 4, 10)
        else:
            return max(base_size - 6, 8)
    
    def _draw_circular_text(
        self, 
        draw: ImageDraw.Draw, 
        text: str, 
        center_x: int, 
        center_y: int, 
        radius: int, 
        font: ImageFont.ImageFont, 
        color: Tuple[int, int, int, int]
    ):
        """Draw text along a circular path"""
        # Calculate angle step for each character
        total_angle = 300  # degrees (leave some space at bottom)
        start_angle = -150  # start angle in degrees
        
        if len(text) > 1:
            angle_step = total_angle / (len(text) - 1)
        else:
            angle_step = 0
        
        for i, char in enumerate(text):
            # Calculate angle for this character
            angle = start_angle + (i * angle_step)
            angle_rad = math.radians(angle)
            
            # Calculate position
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            
            # Get character size for centering
            bbox = draw.textbbox((0, 0), char, font=font)
            char_width = bbox[2] - bbox[0]
            char_height = bbox[3] - bbox[1]
            
            # Draw character centered at calculated position
            draw.text(
                (x - char_width // 2, y - char_height // 2),
                char,
                font=font,
                fill=color
            )
    
    def save_stamp(self, hospital_name: str, filename: str, **kwargs) -> str:
        """
        Generate and save stamp to file
        
        Args:
            hospital_name: Name of the hospital
            filename: Output filename
            **kwargs: Additional parameters for generate_stamp
            
        Returns:
            Path to saved file
        """
        stamp_bytes = self.generate_stamp(hospital_name, **kwargs)
        
        with open(filename, 'wb') as f:
            f.write(stamp_bytes)
        
        return filename