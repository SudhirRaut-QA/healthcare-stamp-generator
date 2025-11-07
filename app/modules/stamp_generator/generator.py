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
    """Pre-defined realistic ink stamp colors"""
    BLUE = (47, 79, 143, 255)      # Realistic ink blue - muted and authentic
    RED = (139, 69, 19, 255)       # Realistic ink red - deep brown-red
    GREEN = (85, 107, 47, 255)     # Realistic ink green - dark olive green
    BLACK = (32, 32, 32, 255)      # Realistic ink black - slightly softer than pure black
    NAVY = (25, 42, 86, 255)       # Realistic navy - deeper and more muted
    MAROON = (101, 67, 33, 255)    # Realistic maroon - earthy brown-red


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
        
        # Calculate optimal text radius - increase for longer text to fit better
        inner_padding = max(8, int(size * 0.04))   # Increased padding: 4% of size, min 8px
        outer_padding = max(8, int(size * 0.04))   # Increased padding: 4% of size, min 8px
        
        # Calculate available space for text positioning after padding
        available_gap = outer_radius - inner_radius
        padded_inner_boundary = inner_radius + inner_padding
        padded_outer_boundary = outer_radius - outer_padding
        
        # For longer text, position closer to outer radius for more circumference
        if text_length > 40:
            # Long text: position at 75% towards outer boundary
            text_radius = int(padded_inner_boundary + (available_gap * 0.75))
        elif text_length > 25:
            # Medium text: position at 65% towards outer boundary  
            text_radius = int(padded_inner_boundary + (available_gap * 0.65))
        else:
            # Short text: position in center of available space
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
        border_style: str = "double",
        character_spacing: float = 2.2  # Optimized: Character spacing multiplier for better readability without overlap
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
            character_spacing: Character spacing multiplier (1.0=normal, 1.4=increased spacing)
            
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
        
        # Draw text with dynamic precision positioning and enhanced character spacing
        text_radius = params['text_radius']  # Use calculated optimal radius
        self._draw_circular_text(
            draw, text_upper, center, center, text_radius, font, color, character_spacing
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
        color: Tuple[int, int, int, int],
        character_spacing_multiplier: float = 1.4  # Balanced default for good spacing
    ):
        """Draw text along a circular path with characters in correct order and proper spacing"""
        
        # 🎛️ SIMPLE MANUAL CONTROLS 🎛️
        # ================================================
        # Change these values to adjust spacing:
        BASE_COVERAGE_ANGLE = 330      # How much of circle to use
        WORD_GAP_SIZE = 8              # Degrees between words
        MIN_CHAR_SPACING = 4.0         # Minimum spacing between characters
        # ================================================
        # Add filled dot symbol before hospital name
        medical_symbol = "●"  # Filled dot symbol
        full_text = f"{medical_symbol} {text}"  # Add symbol only at start
        
        # Calculate text coverage for proper circular appearance
        text_length = len(full_text)
        
        # Calculate word count for better spacing decisions
        word_count = len(full_text.split())
        
        # SIMPLE COVERAGE - Just use the base coverage
        coverage_angle = BASE_COVERAGE_ANGLE
        
        # Simple start angle
        start_angle = -90 - (coverage_angle / 2)
        
        # Split into words for realistic spacing
        words = full_text.split()
        
        # SIMPLE SPACING CALCULATION
        # Calculate total characters (excluding spaces)
        total_chars = len(full_text.replace(' ', ''))
        
        # Calculate total space needed for word gaps
        total_word_gaps = WORD_GAP_SIZE * (word_count - 1) if word_count > 1 else 0
        
        # Remaining space for characters
        char_space = coverage_angle - total_word_gaps
        
        # Simple character spacing
        if total_chars > 0:
            base_char_spacing = char_space / total_chars
        else:
            base_char_spacing = MIN_CHAR_SPACING
        
        # Apply user's multiplier
        realistic_char_spacing = base_char_spacing * character_spacing_multiplier
        
        # Ensure minimum spacing
        realistic_char_spacing = max(MIN_CHAR_SPACING, realistic_char_spacing)
        
        # Draw each word with reduced spacing for justified appearance
        current_angle = start_angle
        
        for word_idx, word in enumerate(words):
            # Simple word spacing
            if word_idx > 0:
                current_angle += WORD_GAP_SIZE
            
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
                
                # Move to next character with consistent spacing
                current_angle += realistic_char_spacing
    
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


# Module-level convenience functions
def generate_stamp(
    hospital_name: str,
    hospital_address: str = "",
    stamp_date: str = "",
    color: StampColor = StampColor.BLUE,
    character_spacing: float = 1.2,
    output_path: str = None,
    **kwargs
) -> str:
    """
    Generate a hospital stamp using the module-level convenience function
    
    Args:
        hospital_name: Name of the hospital
        hospital_address: Address of the hospital (optional)
        stamp_date: Date to include in stamp (optional)
        color: Stamp color from StampColor enum
        character_spacing: Character spacing multiplier for text
        output_path: Path to save the stamp image
        **kwargs: Additional parameters for stamp generation
    
    Returns:
        Path to the generated stamp image
    """
    generator = HospitalStampGenerator()
    
    # Prepare parameters
    params = {
        'color': color.value if isinstance(color, StampColor) else color,
        'character_spacing': character_spacing,
        **kwargs
    }
    
    # Generate stamp
    if output_path:
        return generator.save_stamp_to_output(hospital_name, output_path, **params)
    else:
        # Generate in memory and save with default name
        default_name = f"{hospital_name.replace(' ', '_')}_stamp.png"
        return generator.save_stamp_to_output(hospital_name, default_name, **params)