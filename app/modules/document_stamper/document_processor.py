"""
Document Processor Module
Handles PDF and image file processing for stamp overlay functionality.
"""

import io
import os
from typing import List, Tuple, Union, Optional
from PIL import Image, ImageDraw
import pdf2image
from pdf2image import convert_from_bytes, convert_from_path
import PyPDF2
from io import BytesIO
import base64

class DocumentProcessor:
    """
    Processes documents (PDF, images) for stamp overlay operations.
    Converts documents to images for preview and stamping.
    """
    
    SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif'}
    SUPPORTED_PDF_FORMATS = {'.pdf'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    MAX_IMAGE_DIMENSION = 4000  # Maximum width or height
    
    def __init__(self):
        """Initialize the document processor."""
        self.current_document = None
        self.document_pages = []
        self.document_metadata = {}
    
    def is_supported_format(self, filename: str) -> bool:
        """Check if the file format is supported."""
        ext = os.path.splitext(filename.lower())[1]
        return ext in self.SUPPORTED_IMAGE_FORMATS or ext in self.SUPPORTED_PDF_FORMATS
    
    def load_document(self, file_path: str) -> dict:
        """
        Load document from file path.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Dictionary with document information and pages
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Document not found: {file_path}")
        
        file_size = os.path.getsize(file_path)
        if file_size > self.MAX_FILE_SIZE:
            raise ValueError(f"File too large: {file_size} bytes (max: {self.MAX_FILE_SIZE})")
        
        filename = os.path.basename(file_path)
        if not self.is_supported_format(filename):
            raise ValueError(f"Unsupported file format: {filename}")
        
        ext = os.path.splitext(filename.lower())[1]
        
        if ext == '.pdf':
            return self._load_pdf(file_path)
        else:
            return self._load_image(file_path)
    
    def load_document_from_bytes(self, file_bytes: bytes, filename: str) -> dict:
        """
        Load document from byte data.
        
        Args:
            file_bytes: Document data as bytes
            filename: Original filename for format detection
            
        Returns:
            Dictionary with document information and pages
        """
        if len(file_bytes) > self.MAX_FILE_SIZE:
            raise ValueError(f"File too large: {len(file_bytes)} bytes")
        
        if not self.is_supported_format(filename):
            raise ValueError(f"Unsupported file format: {filename}")
        
        ext = os.path.splitext(filename.lower())[1]
        
        if ext == '.pdf':
            return self._load_pdf_from_bytes(file_bytes, filename)
        else:
            return self._load_image_from_bytes(file_bytes, filename)
    
    def _load_pdf(self, file_path: str) -> dict:
        """Load PDF document and convert pages to images."""
        try:
            # Convert PDF pages to images
            pages = convert_from_path(
                file_path,
                dpi=200,  # Good quality for preview
                first_page=1,
                last_page=None,
                fmt='PNG'
            )
            
            # Get PDF metadata
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                page_count = len(pdf_reader.pages)
                metadata = pdf_reader.metadata or {}
            
            # Process pages
            processed_pages = []
            for i, page_image in enumerate(pages):
                # Resize if too large
                page_image = self._resize_if_needed(page_image)
                
                # Convert to base64 for web display
                img_buffer = BytesIO()
                page_image.save(img_buffer, format='PNG')
                img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
                
                processed_pages.append({
                    'page_number': i + 1,
                    'image': page_image,
                    'base64': f"data:image/png;base64,{img_base64}",
                    'width': page_image.width,
                    'height': page_image.height
                })
            
            self.document_pages = processed_pages
            self.document_metadata = {
                'filename': os.path.basename(file_path),
                'format': 'PDF',
                'page_count': page_count,
                'metadata': dict(metadata) if metadata else {}
            }
            
            return {
                'success': True,
                'document_type': 'PDF',
                'page_count': len(processed_pages),
                'pages': processed_pages,
                'metadata': self.document_metadata
            }
            
        except Exception as e:
            raise Exception(f"Failed to load PDF: {str(e)}")
    
    def _load_pdf_from_bytes(self, file_bytes: bytes, filename: str) -> dict:
        """Load PDF from byte data."""
        try:
            # Convert PDF pages to images
            pages = convert_from_bytes(
                file_bytes,
                dpi=200,
                fmt='PNG'
            )
            
            # Get PDF metadata
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
            page_count = len(pdf_reader.pages)
            metadata = pdf_reader.metadata or {}
            
            # Process pages
            processed_pages = []
            for i, page_image in enumerate(pages):
                page_image = self._resize_if_needed(page_image)
                
                img_buffer = BytesIO()
                page_image.save(img_buffer, format='PNG')
                img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
                
                processed_pages.append({
                    'page_number': i + 1,
                    'image': page_image,
                    'base64': f"data:image/png;base64,{img_base64}",
                    'width': page_image.width,
                    'height': page_image.height
                })
            
            self.document_pages = processed_pages
            self.document_metadata = {
                'filename': filename,
                'format': 'PDF',
                'page_count': page_count,
                'metadata': dict(metadata) if metadata else {}
            }
            
            return {
                'success': True,
                'document_type': 'PDF',
                'page_count': len(processed_pages),
                'pages': processed_pages,
                'metadata': self.document_metadata
            }
            
        except Exception as e:
            raise Exception(f"Failed to load PDF from bytes: {str(e)}")
    
    def _load_image(self, file_path: str) -> dict:
        """Load image document."""
        try:
            image = Image.open(file_path)
            
            # Convert to RGB if needed
            if image.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'RGBA':
                    background.paste(image, mask=image.split()[3])
                else:
                    background.paste(image, mask=image.split()[1])
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize if needed
            image = self._resize_if_needed(image)
            
            # Convert to base64
            img_buffer = BytesIO()
            image.save(img_buffer, format='PNG')
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            
            page_data = {
                'page_number': 1,
                'image': image,
                'base64': f"data:image/png;base64,{img_base64}",
                'width': image.width,
                'height': image.height
            }
            
            self.document_pages = [page_data]
            self.document_metadata = {
                'filename': os.path.basename(file_path),
                'format': 'IMAGE',
                'page_count': 1,
                'dimensions': f"{image.width}x{image.height}"
            }
            
            return {
                'success': True,
                'document_type': 'IMAGE',
                'page_count': 1,
                'pages': [page_data],
                'metadata': self.document_metadata
            }
            
        except Exception as e:
            raise Exception(f"Failed to load image: {str(e)}")
    
    def _load_image_from_bytes(self, file_bytes: bytes, filename: str) -> dict:
        """Load image from byte data."""
        try:
            image = Image.open(BytesIO(file_bytes))
            
            # Convert to RGB if needed
            if image.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'RGBA':
                    background.paste(image, mask=image.split()[3])
                else:
                    background.paste(image, mask=image.split()[1])
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize if needed
            image = self._resize_if_needed(image)
            
            # Convert to base64
            img_buffer = BytesIO()
            image.save(img_buffer, format='PNG')
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            
            page_data = {
                'page_number': 1,
                'image': image,
                'base64': f"data:image/png;base64,{img_base64}",
                'width': image.width,
                'height': image.height
            }
            
            self.document_pages = [page_data]
            self.document_metadata = {
                'filename': filename,
                'format': 'IMAGE',
                'page_count': 1,
                'dimensions': f"{image.width}x{image.height}"
            }
            
            return {
                'success': True,
                'document_type': 'IMAGE',
                'page_count': 1,
                'pages': [page_data],
                'metadata': self.document_metadata
            }
            
        except Exception as e:
            raise Exception(f"Failed to load image from bytes: {str(e)}")
    
    def _resize_if_needed(self, image: Image.Image) -> Image.Image:
        """Resize image if it exceeds maximum dimensions."""
        width, height = image.size
        
        if width <= self.MAX_IMAGE_DIMENSION and height <= self.MAX_IMAGE_DIMENSION:
            return image
        
        # Calculate new dimensions maintaining aspect ratio
        if width > height:
            new_width = self.MAX_IMAGE_DIMENSION
            new_height = int((height * self.MAX_IMAGE_DIMENSION) / width)
        else:
            new_height = self.MAX_IMAGE_DIMENSION
            new_width = int((width * self.MAX_IMAGE_DIMENSION) / height)
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def get_page(self, page_number: int) -> Optional[dict]:
        """Get specific page data."""
        if not self.document_pages or page_number < 1 or page_number > len(self.document_pages):
            return None
        return self.document_pages[page_number - 1]
    
    def get_page_count(self) -> int:
        """Get total number of pages."""
        return len(self.document_pages)
    
    def get_metadata(self) -> dict:
        """Get document metadata."""
        return self.document_metadata