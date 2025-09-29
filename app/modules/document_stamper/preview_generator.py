"""
Preview Generator Module
Generates preview images with stamp overlays for interactive document stamping.
"""

import base64
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageEnhance
from io import BytesIO
import math

from .stamp_overlay import StampOverlay, StampPosition

class PreviewGenerator:
    """
    Generates document previews with stamp overlays.
    Handles rendering stamps on document pages with positioning, scaling, and effects.
    """
    
    def __init__(self, stamp_overlay: StampOverlay):
        """
        Initialize preview generator.
        
        Args:
            stamp_overlay: StampOverlay instance managing stamps
        """
        self.stamp_overlay = stamp_overlay
    
    def generate_page_preview(self, 
                            page_image: Image.Image,
                            page_number: int,
                            preview_width: Optional[int] = None,
                            preview_height: Optional[int] = None,
                            show_boundaries: bool = False) -> dict:
        """
        Generate preview of a page with stamp overlays.
        
        Args:
            page_image: Original page image
            page_number: Page number (1-based)
            preview_width: Target preview width (maintains aspect ratio if only width given)
            preview_height: Target preview height
            show_boundaries: Whether to show stamp boundaries for editing
            
        Returns:
            Dictionary with preview image data and metadata
        """
        # Get page stamps
        page_stamps = self.stamp_overlay.get_page_stamps(page_number)
        
        # Calculate preview dimensions
        original_width, original_height = page_image.size
        
        if preview_width or preview_height:
            if preview_width and not preview_height:
                # Scale by width, maintain aspect ratio
                scale_factor = preview_width / original_width
                preview_height = int(original_height * scale_factor)
            elif preview_height and not preview_width:
                # Scale by height, maintain aspect ratio
                scale_factor = preview_height / original_height
                preview_width = int(original_width * scale_factor)
            else:
                # Both dimensions specified - calculate scale to fit
                width_scale = preview_width / original_width
                height_scale = preview_height / original_height
                scale_factor = min(width_scale, height_scale)
                preview_width = int(original_width * scale_factor)
                preview_height = int(original_height * scale_factor)
        else:
            # Use original dimensions
            preview_width, preview_height = original_width, original_height
            scale_factor = 1.0
        
        # Create preview image
        preview_image = page_image.resize((preview_width, preview_height), Image.Resampling.LANCZOS)
        
        # Apply stamps
        if page_stamps:
            preview_image = self._apply_stamps_to_image(
                preview_image, 
                page_stamps, 
                scale_factor,
                show_boundaries
            )
        
        # Convert to base64
        img_buffer = BytesIO()
        preview_image.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        return {
            'success': True,
            'page_number': page_number,
            'preview_image': preview_image,
            'base64': f"data:image/png;base64,{img_base64}",
            'width': preview_width,
            'height': preview_height,
            'scale_factor': scale_factor,
            'original_dimensions': (original_width, original_height),
            'stamp_count': len(page_stamps),
            'stamps': [stamp.to_dict() for stamp in page_stamps]
        }
    
    def _apply_stamps_to_image(self, 
                              base_image: Image.Image,
                              stamps: List[StampPosition],
                              scale_factor: float,
                              show_boundaries: bool = False) -> Image.Image:
        """
        Apply stamp overlays to an image.
        
        Args:
            base_image: Base image to apply stamps to
            stamps: List of stamp positions
            scale_factor: Scale factor for preview
            show_boundaries: Whether to show stamp boundaries
            
        Returns:
            Image with stamps applied
        """
        # Convert to RGBA for proper blending
        if base_image.mode != 'RGBA':
            result_image = base_image.convert('RGBA')
        else:
            result_image = base_image.copy()
        
        # Sort stamps by z-index (lower first)
        sorted_stamps = sorted(stamps, key=lambda s: s.z_index)
        
        for stamp in sorted_stamps:
            self._apply_single_stamp(result_image, stamp, scale_factor, show_boundaries)
        
        # Convert back to RGB
        if base_image.mode != 'RGBA':
            final_image = Image.new('RGB', result_image.size, (255, 255, 255))
            final_image.paste(result_image, mask=result_image.split()[3] if result_image.mode == 'RGBA' else None)
            return final_image
        
        return result_image
    
    def _apply_single_stamp(self, 
                           target_image: Image.Image,
                           stamp: StampPosition,
                           scale_factor: float,
                           show_boundaries: bool = False):
        """
        Apply a single stamp to the target image.
        
        Args:
            target_image: Target image to modify
            stamp: Stamp position and properties
            scale_factor: Scale factor for preview
            show_boundaries: Whether to show stamp boundaries
        """
        # Get stamp image
        stamp_image = self.stamp_overlay.stamp_images.get(stamp.stamp_id)
        if not stamp_image:
            return
        
        # Calculate actual position and size
        target_width, target_height = target_image.size
        
        # Scale stamp dimensions
        stamp_width = int(stamp.width * scale_factor)
        stamp_height = int(stamp.height * scale_factor)
        
        # Calculate position (center-based)
        stamp_x = int((stamp.x * target_width) - (stamp_width / 2))
        stamp_y = int((stamp.y * target_height) - (stamp_height / 2))
        
        # Ensure stamp stays within bounds
        stamp_x = max(0, min(stamp_x, target_width - stamp_width))
        stamp_y = max(0, min(stamp_y, target_height - stamp_height))
        
        # Resize stamp image
        resized_stamp = stamp_image.resize((stamp_width, stamp_height), Image.Resampling.LANCZOS)
        
        # Apply rotation if needed
        if stamp.rotation != 0:
            resized_stamp = resized_stamp.rotate(
                stamp.rotation, 
                expand=True, 
                fillcolor=(255, 255, 255, 0)
            )
            # Recalculate position after rotation
            new_width, new_height = resized_stamp.size
            stamp_x -= (new_width - stamp_width) // 2
            stamp_y -= (new_height - stamp_height) // 2
            stamp_width, stamp_height = new_width, new_height
        
        # Apply opacity if needed
        if stamp.opacity < 1.0:
            if resized_stamp.mode != 'RGBA':
                resized_stamp = resized_stamp.convert('RGBA')
            
            # Create alpha channel with opacity
            alpha = resized_stamp.split()[3] if resized_stamp.mode == 'RGBA' else Image.new('L', resized_stamp.size, 255)
            alpha = ImageEnhance.Brightness(alpha).enhance(stamp.opacity)
            resized_stamp.putalpha(alpha)
        
        # Paste stamp onto target image
        if resized_stamp.mode == 'RGBA':
            target_image.paste(resized_stamp, (stamp_x, stamp_y), resized_stamp)
        else:
            target_image.paste(resized_stamp, (stamp_x, stamp_y))
        
        # Draw boundaries if requested
        if show_boundaries:
            self._draw_stamp_boundaries(target_image, stamp_x, stamp_y, stamp_width, stamp_height, stamp.stamp_type)
    
    def _draw_stamp_boundaries(self, 
                              target_image: Image.Image,
                              x: int, y: int, width: int, height: int,
                              stamp_type: str):
        """
        Draw stamp boundaries for editing interface.
        
        Args:
            target_image: Target image to draw on
            x, y: Top-left corner position
            width, height: Stamp dimensions
            stamp_type: Type of stamp for color coding
        """
        draw = ImageDraw.Draw(target_image)
        
        # Color code by stamp type
        if stamp_type == 'hospital':
            border_color = (0, 102, 255, 200)  # Blue with transparency
            corner_color = (0, 102, 255, 255)  # Solid blue
        else:  # doctor
            border_color = (255, 102, 0, 200)  # Orange with transparency
            corner_color = (255, 102, 0, 255)  # Solid orange
        
        # Draw border
        draw.rectangle([x, y, x + width - 1, y + height - 1], outline=border_color, width=2)
        
        # Draw corner handles (for resize)
        handle_size = 8
        corners = [
            (x - handle_size//2, y - handle_size//2),  # Top-left
            (x + width - handle_size//2, y - handle_size//2),  # Top-right
            (x - handle_size//2, y + height - handle_size//2),  # Bottom-left
            (x + width - handle_size//2, y + height - handle_size//2)  # Bottom-right
        ]
        
        for corner_x, corner_y in corners:
            draw.rectangle([
                corner_x, corner_y,
                corner_x + handle_size, corner_y + handle_size
            ], fill=corner_color)
    
    def generate_comparison_preview(self, 
                                  page_image: Image.Image,
                                  page_number: int,
                                  preview_width: Optional[int] = None) -> dict:
        """
        Generate side-by-side comparison preview (original vs stamped).
        
        Args:
            page_image: Original page image
            page_number: Page number (1-based)
            preview_width: Target width for each side
            
        Returns:
            Dictionary with comparison preview data
        """
        # Generate original preview
        original_preview = self.generate_page_preview(
            page_image, page_number, preview_width, show_boundaries=False
        )
        
        # Generate stamped preview
        stamped_preview = self.generate_page_preview(
            page_image, page_number, preview_width, show_boundaries=False
        )
        
        # Create side-by-side comparison
        orig_img = original_preview['preview_image']
        stamp_img = stamped_preview['preview_image']
        
        # Create comparison image
        comparison_width = orig_img.width + stamp_img.width + 20  # 20px gap
        comparison_height = max(orig_img.height, stamp_img.height)
        
        comparison_image = Image.new('RGB', (comparison_width, comparison_height), (255, 255, 255))
        
        # Paste images
        comparison_image.paste(orig_img, (0, 0))
        comparison_image.paste(stamp_img, (orig_img.width + 20, 0))
        
        # Add labels
        draw = ImageDraw.Draw(comparison_image)
        draw.text((10, 10), "Original", fill=(0, 0, 0))
        draw.text((orig_img.width + 30, 10), "With Stamps", fill=(0, 0, 0))
        
        # Convert to base64
        img_buffer = BytesIO()
        comparison_image.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        return {
            'success': True,
            'page_number': page_number,
            'comparison_image': comparison_image,
            'base64': f"data:image/png;base64,{img_base64}",
            'width': comparison_width,
            'height': comparison_height,
            'original_width': orig_img.width,
            'stamped_width': stamp_img.width,
            'stamp_count': stamped_preview['stamp_count']
        }
    
    def generate_thumbnail_grid(self, 
                               pages_data: List[dict],
                               thumbnail_size: int = 200,
                               grid_columns: int = 4) -> dict:
        """
        Generate thumbnail grid of all pages with stamp indicators.
        
        Args:
            pages_data: List of page data dictionaries
            thumbnail_size: Size for thumbnails
            grid_columns: Number of columns in grid
            
        Returns:
            Dictionary with grid image data
        """
        if not pages_data:
            return {'success': False, 'error': 'No pages provided'}
        
        # Calculate grid dimensions
        total_pages = len(pages_data)
        grid_rows = math.ceil(total_pages / grid_columns)
        grid_width = grid_columns * (thumbnail_size + 10) - 10
        grid_height = grid_rows * (thumbnail_size + 40) + 20  # Extra space for labels
        
        # Create grid image
        grid_image = Image.new('RGB', (grid_width, grid_height), (245, 245, 245))
        draw = ImageDraw.Draw(grid_image)
        
        for i, page_data in enumerate(pages_data):
            row = i // grid_columns
            col = i % grid_columns
            
            x = col * (thumbnail_size + 10)
            y = row * (thumbnail_size + 40) + 20
            
            # Generate thumbnail with stamps
            page_image = page_data['image']
            page_number = page_data['page_number']
            
            thumbnail_preview = self.generate_page_preview(
                page_image, page_number, thumbnail_size, show_boundaries=False
            )
            
            thumbnail = thumbnail_preview['preview_image']
            
            # Paste thumbnail
            grid_image.paste(thumbnail, (x, y))
            
            # Draw border
            draw.rectangle([x-1, y-1, x + thumbnail_size, y + thumbnail_size], outline=(200, 200, 200))
            
            # Add page label
            label = f"Page {page_number}"
            draw.text((x + 5, y - 18), label, fill=(100, 100, 100))
            
            # Add stamp indicator
            stamp_count = thumbnail_preview['stamp_count']
            if stamp_count > 0:
                # Draw stamp indicator
                indicator_x = x + thumbnail_size - 25
                indicator_y = y + 5
                draw.ellipse([indicator_x, indicator_y, indicator_x + 20, indicator_y + 20], 
                           fill=(0, 150, 0), outline=(255, 255, 255), width=2)
                draw.text((indicator_x + 6, indicator_y + 4), str(stamp_count), fill=(255, 255, 255))
        
        # Convert to base64
        img_buffer = BytesIO()
        grid_image.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        return {
            'success': True,
            'grid_image': grid_image,
            'base64': f"data:image/png;base64,{img_base64}",
            'width': grid_width,
            'height': grid_height,
            'thumbnail_size': thumbnail_size,
            'total_pages': total_pages,
            'total_stamps': sum(self.stamp_overlay.get_stamps_summary()['pages'].values())
        }