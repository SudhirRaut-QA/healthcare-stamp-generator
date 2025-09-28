"""
Hospital Stamp Generator Module
Generates circular hospital stamps with transparent background and customizable features
"""

from PIL import Image, ImageDraw, ImageFont
import io
import math
import os
from datetime import datetime
from typing import Optional, Tuple, Dict, Any
from enum import Enum


class StampStyle(Enum):
    """Stamp style options"""
    CLASSIC = "classic"
    MODERN = "modern"
    OFFICIAL = "official"
    EMERGENCY = "emergency"


class StampColor(Enum):
    """Pre-defined stamp colors"""
    BLUE = (0, 100, 200, 255)
    RED = (200, 50, 50, 255)
    GREEN = (50, 150, 50, 255)
    BLACK = (0, 0, 0, 255)
    NAVY = (25, 25, 112, 255)
    MAROON = (128, 0, 0, 255)


class HospitalStampGenerator:
    """
    Generate circular hospital stamps with transparent background
    """
    
    def __init__(self):
        self.default_size = 300
        self.default_color = StampColor.BLUE.value
        self.background_color = (255, 255, 255, 0)  # Transparent background
        self.output_folder = "stampOutput"
        self.ensure_output_folder()
    
    def ensure_output_folder(self):
        """Ensure output folder exists"""
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
    
    def generate_stamp(
        self, 
        hospital_name: str, 
        size: int = 300,
        font_size: Optional[int] = None,
        color: Optional[Tuple[int, int, int, int]] = None,
        style: StampStyle = StampStyle.CLASSIC,
        include_date: bool = False,
        include_logo: bool = True,
        border_style: str = "double"
    ) -> bytes:
        """
        Generate a circular hospital stamp with enhanced features
        
        Args:
            hospital_name: Name of the hospital
            size: Size of the stamp (diameter in pixels)
            font_size: Font size for text (auto-calculated if None)
            color: RGBA color tuple for the stamp (uses default if None)
            style: Stamp style (CLASSIC, MODERN, OFFICIAL, EMERGENCY)
            include_date: Whether to include current date
            include_logo: Whether to include medical symbol
            border_style: Border style ("single", "double", "triple")
            
        Returns:
            PNG image as bytes
        """
        # Use default color if none provided
        if color is None:
            color = self.default_color
        # Create image with transparent background
        image = Image.new('RGBA', (size, size), self.background_color)
        draw = ImageDraw.Draw(image)
        
        # Calculate circle parameters
        center = size // 2
        radius = center - 10  # Leave some margin
        
        # Draw borders based on style and border_style
        inner_radius = self._draw_borders(draw, center, radius, color, border_style, style)
        
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
        
        # Add center content based on style
        self._draw_center_content(draw, center, font_size, color, style, include_logo, include_date)
        
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
    
    def _draw_borders(self, draw: ImageDraw.Draw, center: int, radius: int, 
                     color: Tuple[int, int, int, int], border_style: str, 
                     style: StampStyle) -> int:
        """Draw stamp borders based on style"""
        if border_style == "single":
            # Single border
            draw.ellipse(
                [center - radius, center - radius, center + radius, center + radius],
                outline=color, width=4
            )
            inner_radius = radius - 25
        elif border_style == "double":
            # Double border (classic)
            border_width = 6 if style == StampStyle.OFFICIAL else 4
            
            # Outer border
            for i in range(border_width):
                draw.ellipse(
                    [center - radius + i, center - radius + i, 
                     center + radius - i, center + radius - i],
                    outline=color, width=1
                )
            
            # Inner border
            inner_radius = radius - 25
            draw.ellipse(
                [center - inner_radius, center - inner_radius,
                 center + inner_radius, center + inner_radius],
                outline=color, width=2
            )
        else:  # triple
            # Triple border for official stamps
            # Outer border
            for i in range(8):
                draw.ellipse(
                    [center - radius + i, center - radius + i, 
                     center + radius - i, center + radius - i],
                    outline=color, width=1
                )
            
            # Middle border
            mid_radius = radius - 15
            draw.ellipse(
                [center - mid_radius, center - mid_radius,
                 center + mid_radius, center + mid_radius],
                outline=color, width=2
            )
            
            # Inner border
            inner_radius = radius - 30
            draw.ellipse(
                [center - inner_radius, center - inner_radius,
                 center + inner_radius, center + inner_radius],
                outline=color, width=1
            )
        
        return inner_radius
    
    def _draw_center_content(self, draw: ImageDraw.Draw, center: int, font_size: int,
                           color: Tuple[int, int, int, int], style: StampStyle,
                           include_logo: bool, include_date: bool):
        """Draw center content based on style"""
        y_offset = 0
        
        if include_logo:
            # Medical symbols based on style
            if style == StampStyle.EMERGENCY:
                symbol = "⚕ EMERGENCY ⚕"
            elif style == StampStyle.OFFICIAL:
                symbol = "⚕ HOSPITAL ⚕"
            elif style == StampStyle.MODERN:
                symbol = "🏥 MEDICAL 🏥"
            else:
                symbol = "★ HOSPITAL ★"
            
            try:
                symbol_font = ImageFont.truetype("arial.ttf", font_size // 2)
            except (OSError, IOError):
                symbol_font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), symbol, font=symbol_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            draw.text(
                (center - text_width // 2, center - text_height // 2 + y_offset),
                symbol,
                font=symbol_font,
                fill=color
            )
            y_offset += text_height + 5
        
        if include_date:
            # Add current date
            current_date = datetime.now().strftime("%d/%m/%Y")
            try:
                date_font = ImageFont.truetype("arial.ttf", font_size // 3)
            except (OSError, IOError):
                date_font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), current_date, font=date_font)
            text_width = bbox[2] - bbox[0]
            
            draw.text(
                (center - text_width // 2, center + y_offset),
                current_date,
                font=date_font,
                fill=color
            )
    
    def generate_enhanced_stamp(self, hospital_name: str, **kwargs) -> bytes:
        """Generate stamp with all enhancements enabled"""
        defaults = {
            'size': 350,
            'style': StampStyle.OFFICIAL,
            'include_date': True,
            'include_logo': True,
            'border_style': 'triple',
            'color': StampColor.NAVY.value
        }
        defaults.update(kwargs)
        return self.generate_stamp(hospital_name, **defaults)
    
    def save_stamp_to_output(self, hospital_name: str, filename: Optional[str] = None, **kwargs) -> str:
        """Save stamp to output folder with automatic naming"""
        if filename is None:
            safe_name = "".join(c for c in hospital_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_name}_{timestamp}.png"
        
        output_path = os.path.join(self.output_folder, filename)
        stamp_bytes = self.generate_stamp(hospital_name, **kwargs)
        
        with open(output_path, 'wb') as f:
            f.write(stamp_bytes)
        
        return output_path
    
    def create_stamp_variants(self, hospital_name: str) -> Dict[str, str]:
        """Create multiple variants of stamps for the same hospital"""
        variants = {}
        
        # Classic blue stamp
        variants['classic'] = self.save_stamp_to_output(
            hospital_name, 
            filename=f"{hospital_name.replace(' ', '_')}_classic.png",
            style=StampStyle.CLASSIC,
            color=StampColor.BLUE.value,
            border_style="double"
        )
        
        # Official navy stamp with date
        variants['official'] = self.save_stamp_to_output(
            hospital_name,
            filename=f"{hospital_name.replace(' ', '_')}_official.png", 
            style=StampStyle.OFFICIAL,
            color=StampColor.NAVY.value,
            border_style="triple",
            include_date=True
        )
        
        # Emergency red stamp
        variants['emergency'] = self.save_stamp_to_output(
            hospital_name,
            filename=f"{hospital_name.replace(' ', '_')}_emergency.png",
            style=StampStyle.EMERGENCY,
            color=StampColor.RED.value,
            border_style="double"
        )
        
        # Modern green stamp
        variants['modern'] = self.save_stamp_to_output(
            hospital_name,
            filename=f"{hospital_name.replace(' ', '_')}_modern.png",
            style=StampStyle.MODERN,
            color=StampColor.GREEN.value,
            border_style="single",
            size=400
        )
        
        return variants