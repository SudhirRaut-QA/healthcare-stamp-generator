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
    
    def _calculate_dynamic_parameters(self, hospital_name: str, size: int) -> Dict[str, Any]:
        """Calculate all dynamic parameters for optimal text fitting with precision"""
        full_text = f"● {hospital_name}"
        text_length = len(full_text)
        word_count = len(full_text.split())
        
        # Dynamic radius calculation based on text complexity
        center = size // 2
        base_radius = center - 20  # Base margin
        
        # Calculate optimal outer radius based on text density
        text_density = text_length / word_count  # Characters per word
        
        if text_length <= 15:
            outer_radius = int(base_radius * 0.75)  # Compact for short text
        elif text_length <= 25:
            outer_radius = int(base_radius * 0.80)  # Medium radius
        elif text_length <= 40:
            outer_radius = int(base_radius * 0.85)  # Larger for long text
        elif text_length <= 60:
            outer_radius = int(base_radius * 0.90)  # Very large
        else:
            outer_radius = int(base_radius * 0.95)  # Maximum radius
        
        # Dynamic gap calculation for perfect text spacing
        if text_length <= 20:
            gap_ratio = 0.35  # Wider gap for short text
        elif text_length <= 40:
            gap_ratio = 0.32  # Medium gap
        else:
            gap_ratio = 0.28  # Narrower gap for long text
        
        radius_gap = max(40, int(outer_radius * gap_ratio))
        inner_radius = outer_radius - radius_gap
        
        # Ensure minimum inner radius
        min_inner_radius = int(size * 0.12)
        if inner_radius < min_inner_radius:
            inner_radius = min_inner_radius
            outer_radius = inner_radius + radius_gap
        
        # Calculate text radius with dynamic padding from both inner and outer circles
        # Add padding to ensure hospital name doesn't touch either boundary
        inner_padding = max(6, int(size * 0.03))   # Padding from inner circle: 3% of size, min 6px
        outer_padding = max(6, int(size * 0.03))   # Padding from outer circle: 3% of size, min 6px
        
        # Calculate available space for text positioning after padding
        available_gap = outer_radius - inner_radius
        padded_inner_boundary = inner_radius + inner_padding
        padded_outer_boundary = outer_radius - outer_padding
        
        # Position text radius in the center of the padded area
        text_radius = (padded_inner_boundary + padded_outer_boundary) // 2
        
        # Ensure text radius is within safe boundaries
        if text_radius < padded_inner_boundary:
            text_radius = padded_inner_boundary
        elif text_radius > padded_outer_boundary:
            text_radius = padded_outer_boundary
        
        # Dynamic font size calculation - Hospital name should be the largest and most prominent
        base_font_size = size // 10  # Increased from size // 12 for larger hospital name
        
        # Adjust font size based on text length and available space (accounting for padding)
        circumference = 2 * math.pi * text_radius
        text_width_needed = text_length * (base_font_size * 0.6)  # Approximate character width
        
        if text_width_needed > circumference * 0.75:  # Text too big for circle (reduced threshold for padding)
            font_size = max(10, int(base_font_size * 0.75))  # More conservative reduction for padding
        elif text_width_needed < circumference * 0.45:  # Text too small (adjusted for padding)
            font_size = min(size // 6, int(base_font_size * 1.2))  # Slightly less aggressive increase
        else:
            font_size = base_font_size
        
        # Dynamic spacing calculation
        available_circumference = circumference * 0.85  # Use 85% of circle
        char_spacing_degrees = (available_circumference / text_length) * (360 / circumference)
        
        # Ensure minimum spacing
        char_spacing_degrees = max(4, char_spacing_degrees)
        
        return {
            'outer_radius': outer_radius,
            'inner_radius': inner_radius,
            'text_radius': text_radius,
            'font_size': font_size,
            'char_spacing': char_spacing_degrees,
            'gap_width': radius_gap,
            'text_length': text_length,
            'word_count': word_count
        }
    
    def _calculate_optimal_radius(self, hospital_name: str, size: int) -> Tuple[int, int]:
        """Legacy method for backward compatibility"""
        params = self._calculate_dynamic_parameters(hospital_name, size)
        return params['outer_radius'], params['inner_radius']

    def _load_realistic_font(self, font_size: int) -> ImageFont.ImageFont:
        """
        Load realistic medical stamp fonts with comprehensive fallback system
        
        Prioritizes fonts that look like authentic medical/official stamps:
        1. Times New Roman - Classic, professional serif font
        2. Georgia - Elegant serif, excellent readability
        3. Liberation Serif - Open source Times alternative
        4. DejaVu Serif - Cross-platform serif font
        5. Arial Black - Bold, impactful sans-serif
        6. Trebuchet MS - Clean, professional sans-serif
        7. Calibri - Modern, clean Microsoft font
        8. Verdana - High readability sans-serif
        9. Arial/Arial.ttf - Standard fallback
        10. Default system font
        """
        
        # Realistic medical stamp fonts in order of preference
        realistic_fonts = [
            # Serif fonts (more traditional, professional stamp look)
            "times.ttf",           # Times New Roman - Windows
            "Times New Roman.ttf", # Times New Roman - Alternative
            "timesnr.ttf",         # Times New Roman - Windows variant
            "georgia.ttf",         # Georgia - Windows
            "Georgia.ttf",         # Georgia - Alternative
            "LiberationSerif-Regular.ttf",  # Open source Times alternative
            "DejaVuSerif.ttf",     # Cross-platform serif
            "DejaVuSerif-Bold.ttf", # Bold variant for more impact
            
            # Bold sans-serif fonts (modern stamp look)
            "ariblk.ttf",          # Arial Black - Windows
            "Arial Black.ttf",     # Arial Black - Alternative
            "trebucbd.ttf",        # Trebuchet MS Bold - Windows
            "Trebuchet MS Bold.ttf", # Trebuchet MS Bold - Alternative
            "calibrib.ttf",        # Calibri Bold - Windows
            "Calibri Bold.ttf",    # Calibri Bold - Alternative
            
            # Clean, readable fonts
            "verdana.ttf",         # Verdana - Windows
            "Verdana.ttf",         # Verdana - Alternative
            "trebuc.ttf",          # Trebuchet MS - Windows
            "Trebuchet MS.ttf",    # Trebuchet MS - Alternative
            "calibri.ttf",         # Calibri - Windows
            "Calibri.ttf",         # Calibri - Alternative
            
            # Standard fallbacks
            "arial.ttf",           # Arial - Windows
            "Arial.ttf",           # Arial - Alternative
            "ArialMT.ttf",         # Arial - macOS
            "helvetica.ttf",       # Helvetica - Alternative
            "Helvetica.ttf"        # Helvetica - macOS/Linux
        ]
        
        # Try each font in order of preference
        for font_name in realistic_fonts:
            try:
                font = ImageFont.truetype(font_name, font_size)
                # Successfully loaded font
                return font
            except (OSError, IOError):
                continue
        
        # If no TrueType fonts available, try to get a better default
        try:
            # Try to load default with larger size for better appearance
            return ImageFont.load_default()
        except:
            # Absolute fallback - create a basic font
            return ImageFont.load_default()

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
        
        # Calculate all dynamic parameters for optimal fitting
        center = size // 2
        params = self._calculate_dynamic_parameters(hospital_name, size)
        outer_radius = params['outer_radius']
        inner_radius = params['inner_radius']
        
        # Draw borders based on style and border_style
        self._draw_borders(draw, center, outer_radius, inner_radius, color, border_style, style)
        
        # Use calculated dynamic font size
        if font_size is None:
            font_size = params['font_size']
        
        # Load realistic medical stamp font with comprehensive fallback system
        font = self._load_realistic_font(font_size)
        
        # Prepare text for circular arrangement
        text_upper = hospital_name.upper()
        
        # Draw text with dynamic precision positioning
        text_radius = params['text_radius']  # Use calculated optimal radius
        self._draw_circular_text(
            draw, text_upper, center, center, text_radius, font, color
        )
        
        # Add center content with horizontal dividing line and PAID/Online-Offline text
        self._draw_center_content(draw, center, inner_radius, font_size, color, style, include_logo, include_date)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG', optimize=True)
        img_byte_arr.seek(0)
        
        return img_byte_arr.getvalue()
    
    def _calculate_font_size(self, text: str, stamp_size: int) -> int:
        """Calculate dynamic font size - now integrated into _calculate_dynamic_parameters"""
        params = self._calculate_dynamic_parameters(text, stamp_size)
        return params['font_size']
    
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
        """Draw text along a circular path with characters in correct order"""
        # Add filled dot symbol before hospital name
        medical_symbol = "●"  # Filled dot symbol
        full_text = f"{medical_symbol} {text}"  # Add symbol only at start
        
        # Calculate text coverage for proper circular appearance
        text_length = len(full_text)
        
        # Calculate word count for better spacing decisions
        word_count = len(full_text.split())
        
        # DYNAMIC CIRCLE FILLING - Use full available space
        # Always use maximum coverage with small gap for visual balance
        coverage_angle = 350  # Use almost full circle (10° gap for balance)
        
        # For very short text, use slightly less to prevent over-spreading
        if text_length <= 6:
            coverage_angle = 320  # Don't over-spread very short text
        elif text_length <= 12:
            coverage_angle = 340  # Moderate coverage for short text
        
        # The text will now ALWAYS fill the available space dynamically
        
        # Calculate character spacing with word count adjustment
        char_spacing = coverage_angle / text_length if text_length > 0 else 10
        
        # Adjust minimum spacing based on word count
        if word_count > 5:
            min_spacing = 6  # Tighter spacing for many words
        elif word_count > 3:
            min_spacing = 7  # Medium spacing
        else:
            min_spacing = 8  # Standard spacing
        
        # Ensure minimum spacing for readability
        char_spacing = max(char_spacing, min_spacing)
        
        # Start angle (centered at top)
        start_angle = -90 - (coverage_angle / 2)
        
        # Split into words for realistic spacing
        words = full_text.split()
        
        # TRULY DYNAMIC SPACING - Fill the entire available circle
        
        # Calculate total characters (excluding spaces)
        total_chars = len(full_text.replace(' ', ''))
        
        # Reserve space for word gaps (smaller, proportional gaps)
        word_gap_ratio = 1.5  # Words are 1.5x character spacing apart
        total_word_gaps = (len(words) - 1) * word_gap_ratio
        
        # Calculate dynamic character spacing to fill the entire coverage angle
        # This ensures NO empty space between end and start
        effective_units = total_chars + total_word_gaps  # Total spacing units needed
        realistic_char_spacing = coverage_angle / effective_units if effective_units > 0 else 10
        
        # Apply reasonable bounds (not too tight, not too loose)
        min_spacing = 3.0  # Minimum for readability
        max_spacing = 25.0  # Maximum to prevent over-spreading short text
        realistic_char_spacing = max(min_spacing, min(realistic_char_spacing, max_spacing))
        
        # Draw each word with dynamic spacing
        current_angle = start_angle
        
        for word_idx, word in enumerate(words):
            # Add dynamic spacing between words (proportional to character spacing)
            if word_idx > 0:
                current_angle += realistic_char_spacing * word_gap_ratio
            
            # Draw characters in word with tight, realistic spacing
            for char_idx, char in enumerate(word):
                # Calculate position on circle
                angle_rad = math.radians(current_angle)
                x = center_x + radius * math.cos(angle_rad)
                y = center_y + radius * math.sin(angle_rad)
                
                # Get character dimensions
                bbox = draw.textbbox((0, 0), char, font=font)
                char_width = bbox[2] - bbox[0]
                char_height = bbox[3] - bbox[1]
                
                # Create temporary image for rotation
                temp_size = max(char_width, char_height) + 30
                temp_img = Image.new('RGBA', (temp_size, temp_size), (0, 0, 0, 0))
                temp_draw = ImageDraw.Draw(temp_img)
                
                # Draw character in center with bold effect
                bold_offsets = [(0, 0), (1, 0), (0, 1), (1, 1)]
                char_x = temp_size // 2 - char_width // 2
                char_y = temp_size // 2 - char_height // 2
                
                for dx, dy in bold_offsets:
                    temp_draw.text(
                        (char_x + dx, char_y + dy),
                        char,
                        font=font,
                        fill=color
                    )
                
                # Rotate character to follow curve (tangent to circle)
                rotation_angle = current_angle + 90  # Perpendicular to radius
                rotated_char = temp_img.rotate(-rotation_angle, expand=True)
                
                # Paste rotated character
                rotated_width, rotated_height = rotated_char.size
                paste_x = int(x - rotated_width // 2)
                paste_y = int(y - rotated_height // 2)
                
                # Handle transparency
                if rotated_char.mode == 'RGBA':
                    r, g, b, a = rotated_char.split()
                    mask = a
                else:
                    mask = None
                
                # Paste onto main image
                main_img = draw._image
                main_img.paste(rotated_char, (paste_x, paste_y), mask)
                
                # Move to next character with dynamic readable spacing
                if char == medical_symbol:
                    current_angle += realistic_char_spacing * 1.5  # Proper space after dot
                else:
                    # Dynamic character spacing within words - readable but natural
                    if char in 'ILil|1':  # Narrow characters
                        spacing_multiplier = 0.8  # Slightly closer for narrow chars
                    elif char in 'MW@':   # Wide characters  
                        spacing_multiplier = 1.2  # More space for wide chars
                    else:  # Normal characters
                        spacing_multiplier = 1.0  # Standard readable spacing
                    
                    current_angle += realistic_char_spacing * spacing_multiplier
    
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
    
    def _draw_borders(self, draw: ImageDraw.Draw, center: int, outer_radius: int, inner_radius: int,
                     color: Tuple[int, int, int, int], border_style: str, 
                     style: StampStyle):
        """Draw two circular lines - outer thick, inner thin with optimal spacing"""
        
        # Outer thick border (much broader)
        outer_thickness = 12 if style == StampStyle.OFFICIAL else 10
        for i in range(outer_thickness):
            draw.ellipse(
                [center - outer_radius + i, center - outer_radius + i, 
                 center + outer_radius - i, center + outer_radius - i],
                outline=color, width=1
            )
        
        # Inner thin border - perfectly positioned based on calculations
        draw.ellipse(
            [center - inner_radius, center - inner_radius,
             center + inner_radius, center + inner_radius],
            outline=color, width=2
        )
    
    def _draw_center_content(self, draw: ImageDraw.Draw, center: int, inner_radius: int, 
                           font_size: int, color: Tuple[int, int, int, int], style: StampStyle,
                           include_logo: bool, include_date: bool):
        """Draw center content with two horizontal lines creating sections: PAID and CASH/Online (no dates)"""
        
        # Calculate dynamic spacing for realistic appearance
        realistic_spacing = inner_radius * 0.25  # 25% of radius for generous spacing between PAID and line
        
        # Lines positioned within inner circle boundaries with proper margins
        line_margin = inner_radius * 0.1  # 10% margin from circle edge
        line_start_x = center - inner_radius + line_margin    # Start inside circle
        line_end_x = center + inner_radius - line_margin      # End inside circle
        
        # Calculate dynamic font sizes based on inner circle size with proper hierarchy
        # Hospital name is largest, PAID is medium, CASH/Online is smallest
        paid_font_size = max(int(inner_radius * 0.35), 10)   # Reduced from 0.45 to be smaller than hospital name
        status_font_size = max(int(inner_radius * 0.22), 8)  # Reduced from 0.28 to be smallest
        
        # Load realistic fonts for inner circle text
        paid_font = self._load_realistic_font(paid_font_size)
        status_font = self._load_realistic_font(status_font_size)
        
        # 1. Draw "PAID" text in upper section with generous spacing
        paid_text = "PAID"
        paid_bbox = draw.textbbox((0, 0), paid_text, font=paid_font)
        paid_width = paid_bbox[2] - paid_bbox[0]
        paid_height = paid_bbox[3] - paid_bbox[1]
        
        # Position PAID text in upper area with realistic spacing from first line
        paid_y = center - inner_radius + (inner_radius * 0.3)  # 30% down from top
        paid_x = center - (paid_width / 2)
        
        # Ensure PAID stays within circle bounds
        circle_top_bound = center - inner_radius + (inner_radius * 0.15)
        if paid_y < circle_top_bound:
            paid_y = circle_top_bound
        
        # Draw PAID text with bold effect (multiple passes for thickness)
        bold_offsets = [(0, 0), (1, 0), (0, 1), (1, 1)]
        for dx, dy in bold_offsets:
            draw.text(
                (paid_x + dx, paid_y + dy),
                paid_text,
                font=paid_font,
                fill=color
            )
        
        # 2. Draw first horizontal line with realistic spacing below PAID
        first_line_y = paid_y + paid_height + realistic_spacing
        
        # Ensure line stays within circle bounds
        max_first_line_y = center - (inner_radius * 0.1)
        if first_line_y > max_first_line_y:
            first_line_y = max_first_line_y
        
        # Draw first horizontal line (full width attached to circle)
        draw.line(
            [(line_start_x, first_line_y), (line_end_x, first_line_y)],
            fill=color[:3],  # Remove alpha for line drawing
            width=max(2, inner_radius // 20)  # Dynamic line width, minimum 2px
        )
        
        # 3. Draw "CASH / Online" text in middle section
        status_text = "CASH / Online"
        status_bbox = draw.textbbox((0, 0), status_text, font=status_font)
        status_width = status_bbox[2] - status_bbox[0]
        status_height = status_bbox[3] - status_bbox[1]
        
        # Position status text between first and second lines
        status_y = first_line_y + (inner_radius * 0.15) + (status_height / 2)
        status_x = center - (status_width / 2)
        
        # Ensure status text stays within reasonable bounds
        max_status_y = center + (inner_radius * 0.1)  # Keep closer to center
        if status_y > max_status_y:
            status_y = max_status_y
        
        # Draw status text with enhanced visibility (bold effect)
        # Use multiple passes for bold appearance like PAID text
        bold_offsets = [(0, 0), (1, 0), (0, 1), (1, 1)]
        for dx, dy in bold_offsets:
            draw.text(
                (status_x + dx, status_y + dy),
                status_text,
                font=status_font,
                fill=color
            )
        
        # 4. Draw second horizontal line below status text
        # Position second line with proper spacing, ensuring it stays well within circle
        second_line_y = status_y + status_height + (inner_radius * 0.12)  # Reduced spacing
        
        # Ensure second line stays well within circle bounds (30% margin from bottom)
        max_second_line_y = center + inner_radius - (inner_radius * 0.3)  # More conservative margin
        if second_line_y > max_second_line_y:
            second_line_y = max_second_line_y
        
        # Draw second horizontal line (full width attached to circle)
        draw.line(
            [(line_start_x, second_line_y), (line_end_x, second_line_y)],
            fill=color[:3],  # Remove alpha for line drawing
            width=max(2, inner_radius // 20)  # Dynamic line width, minimum 2px
        )
        
        # Note: Date functionality removed as requested
        # The bottom section between second line and circle edge remains empty for clean appearance
    
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