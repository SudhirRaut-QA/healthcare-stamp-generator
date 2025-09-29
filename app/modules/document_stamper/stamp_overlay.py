"""
Stamp Overlay Module
Handles placing, resizing, and managing stamps on document pages.
"""

import uuid
from typing import List, Dict, Tuple, Optional, Union
from PIL import Image, ImageDraw
from dataclasses import dataclass
import json
import base64
from io import BytesIO

@dataclass
class StampPosition:
    """Represents a stamp's position and properties on a document page."""
    stamp_id: str
    stamp_type: str  # 'hospital' or 'doctor'
    x: float  # X coordinate (0-1 normalized)
    y: float  # Y coordinate (0-1 normalized)
    width: int  # Stamp width in pixels
    height: int  # Stamp height in pixels
    rotation: float = 0.0  # Rotation angle in degrees
    opacity: float = 1.0  # Opacity (0.0-1.0)
    z_index: int = 1  # Layer order
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'stamp_id': self.stamp_id,
            'stamp_type': self.stamp_type,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'rotation': self.rotation,
            'opacity': self.opacity,
            'z_index': self.z_index
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'StampPosition':
        """Create from dictionary."""
        return cls(**data)

class StampOverlay:
    """
    Manages stamp overlays on document pages.
    Handles adding, positioning, resizing, and removing stamps.
    """
    
    def __init__(self):
        """Initialize the stamp overlay manager."""
        self.stamps_by_page = {}  # page_number -> List[StampPosition]
        self.stamp_images = {}    # stamp_id -> PIL Image
        self.stamp_data = {}      # stamp_id -> stamp generation data
    
    def add_stamp(self, 
                  page_number: int,
                  stamp_type: str,
                  stamp_image: Image.Image,
                  stamp_data: dict,
                  x: float = 0.5,
                  y: float = 0.5,
                  width: Optional[int] = None,
                  height: Optional[int] = None) -> str:
        """
        Add a stamp to a specific page.
        
        Args:
            page_number: Page number (1-based)
            stamp_type: Type of stamp ('hospital' or 'doctor')
            stamp_image: PIL Image of the stamp
            stamp_data: Original stamp generation data
            x: X position (0-1 normalized, 0.5 = center)
            y: Y position (0-1 normalized, 0.5 = center)
            width: Stamp width (if None, use original)
            height: Stamp height (if None, use original)
            
        Returns:
            Unique stamp ID
        """
        stamp_id = str(uuid.uuid4())
        
        # Use original dimensions if not specified
        if width is None:
            width = stamp_image.width
        if height is None:
            height = stamp_image.height
        
        # Create stamp position
        stamp_position = StampPosition(
            stamp_id=stamp_id,
            stamp_type=stamp_type,
            x=x,
            y=y,
            width=width,
            height=height
        )
        
        # Store stamp data
        self.stamp_images[stamp_id] = stamp_image
        self.stamp_data[stamp_id] = stamp_data
        
        # Add to page
        if page_number not in self.stamps_by_page:
            self.stamps_by_page[page_number] = []
        
        self.stamps_by_page[page_number].append(stamp_position)
        
        return stamp_id
    
    def move_stamp(self, stamp_id: str, x: float, y: float) -> bool:
        """
        Move a stamp to new position.
        
        Args:
            stamp_id: Unique stamp identifier
            x: New X position (0-1 normalized)
            y: New Y position (0-1 normalized)
            
        Returns:
            True if stamp was found and moved
        """
        for page_stamps in self.stamps_by_page.values():
            for stamp in page_stamps:
                if stamp.stamp_id == stamp_id:
                    stamp.x = max(0.0, min(1.0, x))
                    stamp.y = max(0.0, min(1.0, y))
                    return True
        return False
    
    def resize_stamp(self, stamp_id: str, width: int, height: int) -> bool:
        """
        Resize a stamp.
        
        Args:
            stamp_id: Unique stamp identifier
            width: New width in pixels
            height: New height in pixels
            
        Returns:
            True if stamp was found and resized
        """
        for page_stamps in self.stamps_by_page.values():
            for stamp in page_stamps:
                if stamp.stamp_id == stamp_id:
                    stamp.width = max(50, min(800, width))  # Limit size
                    stamp.height = max(50, min(800, height))
                    return True
        return False
    
    def rotate_stamp(self, stamp_id: str, rotation: float) -> bool:
        """
        Rotate a stamp.
        
        Args:
            stamp_id: Unique stamp identifier
            rotation: Rotation angle in degrees
            
        Returns:
            True if stamp was found and rotated
        """
        for page_stamps in self.stamps_by_page.values():
            for stamp in page_stamps:
                if stamp.stamp_id == stamp_id:
                    stamp.rotation = rotation % 360
                    return True
        return False
    
    def set_stamp_opacity(self, stamp_id: str, opacity: float) -> bool:
        """
        Set stamp opacity.
        
        Args:
            stamp_id: Unique stamp identifier
            opacity: Opacity value (0.0-1.0)
            
        Returns:
            True if stamp was found and opacity was set
        """
        for page_stamps in self.stamps_by_page.values():
            for stamp in page_stamps:
                if stamp.stamp_id == stamp_id:
                    stamp.opacity = max(0.0, min(1.0, opacity))
                    return True
        return False
    
    def set_stamp_z_index(self, stamp_id: str, z_index: int) -> bool:
        """
        Set stamp layer order.
        
        Args:
            stamp_id: Unique stamp identifier
            z_index: Layer order (higher = on top)
            
        Returns:
            True if stamp was found and z-index was set
        """
        for page_stamps in self.stamps_by_page.values():
            for stamp in page_stamps:
                if stamp.stamp_id == stamp_id:
                    stamp.z_index = z_index
                    return True
        return False
    
    def remove_stamp(self, stamp_id: str) -> bool:
        """
        Remove a stamp.
        
        Args:
            stamp_id: Unique stamp identifier
            
        Returns:
            True if stamp was found and removed
        """
        for page_number, page_stamps in self.stamps_by_page.items():
            for i, stamp in enumerate(page_stamps):
                if stamp.stamp_id == stamp_id:
                    # Remove from page
                    del page_stamps[i]
                    
                    # Clean up stamp data
                    if stamp_id in self.stamp_images:
                        del self.stamp_images[stamp_id]
                    if stamp_id in self.stamp_data:
                        del self.stamp_data[stamp_id]
                    
                    return True
        return False
    
    def get_page_stamps(self, page_number: int) -> List[StampPosition]:
        """
        Get all stamps on a specific page.
        
        Args:
            page_number: Page number (1-based)
            
        Returns:
            List of stamp positions, sorted by z-index
        """
        stamps = self.stamps_by_page.get(page_number, [])
        return sorted(stamps, key=lambda s: s.z_index)
    
    def get_stamp_info(self, stamp_id: str) -> Optional[dict]:
        """
        Get complete stamp information.
        
        Args:
            stamp_id: Unique stamp identifier
            
        Returns:
            Dictionary with stamp position and data, or None if not found
        """
        for page_number, page_stamps in self.stamps_by_page.items():
            for stamp in page_stamps:
                if stamp.stamp_id == stamp_id:
                    return {
                        'position': stamp.to_dict(),
                        'data': self.stamp_data.get(stamp_id, {}),
                        'page_number': page_number
                    }
        return None
    
    def clear_page_stamps(self, page_number: int) -> int:
        """
        Remove all stamps from a page.
        
        Args:
            page_number: Page number (1-based)
            
        Returns:
            Number of stamps removed
        """
        if page_number not in self.stamps_by_page:
            return 0
        
        stamps = self.stamps_by_page[page_number]
        count = len(stamps)
        
        # Clean up stamp data
        for stamp in stamps:
            stamp_id = stamp.stamp_id
            if stamp_id in self.stamp_images:
                del self.stamp_images[stamp_id]
            if stamp_id in self.stamp_data:
                del self.stamp_data[stamp_id]
        
        # Clear page
        self.stamps_by_page[page_number] = []
        
        return count
    
    def clear_all_stamps(self) -> int:
        """
        Remove all stamps from all pages.
        
        Returns:
            Total number of stamps removed
        """
        total_count = sum(len(stamps) for stamps in self.stamps_by_page.values())
        
        # Clear all data
        self.stamps_by_page.clear()
        self.stamp_images.clear()
        self.stamp_data.clear()
        
        return total_count
    
    def get_stamps_summary(self) -> dict:
        """
        Get summary of all stamps.
        
        Returns:
            Dictionary with stamp statistics and page information
        """
        total_stamps = sum(len(stamps) for stamps in self.stamps_by_page.values())
        pages_with_stamps = len([p for p, stamps in self.stamps_by_page.items() if stamps])
        
        stamp_types = {}
        for stamps in self.stamps_by_page.values():
            for stamp in stamps:
                stamp_types[stamp.stamp_type] = stamp_types.get(stamp.stamp_type, 0) + 1
        
        return {
            'total_stamps': total_stamps,
            'pages_with_stamps': pages_with_stamps,
            'stamp_types': stamp_types,
            'pages': {
                page_num: len(stamps) 
                for page_num, stamps in self.stamps_by_page.items()
                if stamps
            }
        }
    
    def export_stamps_config(self) -> str:
        """
        Export stamp configuration as JSON.
        
        Returns:
            JSON string with all stamp positions and metadata
        """
        config = {
            'version': '1.0',
            'stamps_by_page': {
                str(page_num): [stamp.to_dict() for stamp in stamps]
                for page_num, stamps in self.stamps_by_page.items()
            },
            'stamp_data': self.stamp_data
        }
        return json.dumps(config, indent=2)
    
    def import_stamps_config(self, config_json: str) -> bool:
        """
        Import stamp configuration from JSON.
        
        Args:
            config_json: JSON string with stamp configuration
            
        Returns:
            True if import was successful
        """
        try:
            config = json.loads(config_json)
            
            # Clear existing data
            self.clear_all_stamps()
            
            # Import stamp positions
            for page_str, stamps_data in config.get('stamps_by_page', {}).items():
                page_num = int(page_str)
                self.stamps_by_page[page_num] = [
                    StampPosition.from_dict(stamp_data) 
                    for stamp_data in stamps_data
                ]
            
            # Import stamp data
            self.stamp_data = config.get('stamp_data', {})
            
            return True
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            return False