"""
Document Processor Module
Handles PDF and image file processing for stamp overlay functionality.
"""

import io
import os
import subprocess
import sys
from typing import List, Tuple, Union, Optional
from PIL import Image, ImageDraw
import PyPDF2
from io import BytesIO
import base64

# Try to import PDF processing libraries
try:
    import pdf2image
    from pdf2image import convert_from_bytes, convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False
    convert_from_bytes = None
    convert_from_path = None

# Try to import PyMuPDF as an alternative
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

# Portable Poppler configuration
def get_portable_poppler_path():
    """Get the path to portable Poppler if available."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..', '..')
    poppler_path = os.path.join(project_root, 'tools', 'poppler-23.08.0', 'Library', 'bin')
    
    if os.path.exists(poppler_path) and os.path.exists(os.path.join(poppler_path, 'pdftoppm.exe')):
        return poppler_path
    return None

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
        self.filename = None
    
    def is_supported_format(self, filename: str) -> bool:
        """Check if the file format is supported."""
        ext = os.path.splitext(filename.lower())[1]
        return ext in self.SUPPORTED_IMAGE_FORMATS or ext in self.SUPPORTED_PDF_FORMATS
    
    def _check_poppler_installation(self) -> bool:
        """Check if Poppler is installed and available."""
        try:
            # Check for portable poppler first
            portable_path = get_portable_poppler_path()
            if portable_path:
                return True
            
            # Check if pdftoppm is available in PATH
            subprocess.run(['pdftoppm', '-h'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _convert_pdf_with_pymupdf(self, file_bytes: bytes) -> List[Image.Image]:
        """Convert PDF pages to images using PyMuPDF."""
        if not PYMUPDF_AVAILABLE:
            raise ImportError("PyMuPDF not available")
        
        images = []
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # Convert to image with high DPI for quality
            mat = fitz.Matrix(2.0, 2.0)  # 2x scaling for better quality
            pix = page.get_pixmap(matrix=mat)
            
            # Convert PyMuPDF pixmap to PIL Image
            img_data = pix.tobytes("png")
            img = Image.open(BytesIO(img_data))
            images.append(img)
        
        doc.close()
        return images
    
    def _convert_pdf_from_path_with_pymupdf(self, file_path: str) -> List[Image.Image]:
        """Convert PDF pages to images using PyMuPDF from file path."""
        if not PYMUPDF_AVAILABLE:
            raise ImportError("PyMuPDF not available")
        
        images = []
        doc = fitz.open(file_path)
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # Convert to image with high DPI for quality
            mat = fitz.Matrix(2.0, 2.0)  # 2x scaling for better quality
            pix = page.get_pixmap(matrix=mat)
            
            # Convert PyMuPDF pixmap to PIL Image
            img_data = pix.tobytes("png")
            img = Image.open(BytesIO(img_data))
            images.append(img)
        
        doc.close()
        return images
    
    def _sanitize_pdf_metadata(self, metadata) -> dict:
        """
        Sanitize PDF metadata to make it JSON serializable.
        
        Args:
            metadata: Raw PDF metadata from PyPDF2
            
        Returns:
            Dictionary with sanitized metadata
        """
        if not metadata:
            return {}
        
        sanitized = {}
        for key, value in metadata.items():
            try:
                # Remove leading '/' from keys
                clean_key = key.lstrip('/')
                
                # Convert PyPDF2 objects to strings
                if hasattr(value, '__str__'):
                    sanitized[clean_key] = str(value)
                else:
                    sanitized[clean_key] = value
            except Exception:
                # Skip problematic metadata entries
                continue
        
        return sanitized
    
    def _create_pdf_placeholder_image(self, page_count: int, filename: str) -> List[dict]:
        """
        Create placeholder images for PDF pages when Poppler is not available.
        
        Args:
            page_count: Number of pages in PDF
            filename: PDF filename
            
        Returns:
            List of page dictionaries with placeholder images
        """
        processed_pages = []
        
        for page_num in range(1, page_count + 1):
            # Create professional document placeholder
            width, height = 595, 842  # A4 size in pixels at 72 DPI
            
            # Create white background
            image = Image.new('RGB', (width, height), 'white')
            draw = ImageDraw.Draw(image)
            
            # Professional document styling
            header_color = '#2c3e50'
            content_color = '#34495e'
            stamp_zone_color = '#ecf0f1'
            border_color = '#bdc3c7'
            
            # Draw document border
            draw.rectangle([20, 20, width-20, height-20], outline=border_color, width=2)
            
            # Header section
            draw.rectangle([40, 40, width-40, 120], fill='#f8f9fa', outline=border_color)
            
            # Document title
            title_text = f"{filename} - Page {page_num}"
            draw.text((60, 60), title_text, fill=header_color)
            draw.text((60, 85), f"Professional Document Preview", fill=content_color)
            
            # Content lines simulation
            line_y = 160
            for i in range(15):
                line_width = 400 if i % 3 != 2 else 250  # Varying line lengths
                draw.rectangle([60, line_y, 60 + line_width, line_y + 8], fill=content_color)
                line_y += 25
            
            # Stamp placement zones
            stamp_zones = [
                (450, 200, 550, 260),  # Top right
                (450, 400, 550, 460),  # Middle right  
                (450, 650, 550, 710),  # Bottom right
            ]
            
            for zone in stamp_zones:
                draw.rectangle(zone, fill=stamp_zone_color, outline=border_color)
                center_x = (zone[0] + zone[2]) // 2
                center_y = (zone[1] + zone[3]) // 2
                draw.text((center_x-25, center_y-5), "STAMP", fill='#7f8c8d')
            
            # Footer
            draw.text((60, height-60), f"Page {page_num} of {page_count}", fill='#95a5a6')
            draw.text((60, height-40), "PDF preview requires Poppler for full document display", fill='#e74c3c')
            
            # Convert to base64
            img_buffer = BytesIO()
            image.save(img_buffer, format='PNG')
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            
            processed_pages.append({
                'page_number': page_num,
                'image': image,
                'base64': f"data:image/png;base64,{img_base64}",
                'width': width,
                'height': height
            })
        
        return processed_pages
    
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
            # Get PDF metadata first
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                page_count = len(pdf_reader.pages)
                metadata = pdf_reader.metadata or {}
            
            processed_pages = []
            
            # Try PyMuPDF first (pure Python, no external dependencies)
            if PYMUPDF_AVAILABLE:
                try:
                    pages = self._convert_pdf_from_path_with_pymupdf(file_path)
                    
                    # Process pages
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
                    
                    print(f"✅ PDF converted using PyMuPDF: {len(processed_pages)} pages")
                        
                except Exception as pymupdf_error:
                    print(f"PyMuPDF conversion failed: {pymupdf_error}")
                    processed_pages = []
            
            # Try pdf2image with Poppler if PyMuPDF failed
            if not processed_pages and PDF2IMAGE_AVAILABLE and self._check_poppler_installation():
                try:
                    # Convert PDF pages to images
                    pages = convert_from_path(
                        file_path,
                        dpi=200,  # Good quality for preview
                        first_page=1,
                        last_page=None,
                        fmt='PNG'
                    )
                    
                    # Process pages
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
                    
                    print(f"✅ PDF converted using Poppler: {len(processed_pages)} pages")
                        
                except Exception as pdf_convert_error:
                    print(f"PDF conversion failed: {pdf_convert_error}")
                    processed_pages = []
            
            # Fall back to placeholder images if both methods failed
            if not processed_pages:
                processed_pages = self._create_pdf_placeholder_image(page_count, os.path.basename(file_path))
                print(f"📄 Using placeholder images: {len(processed_pages)} pages")
            
            self.document_pages = processed_pages
            self.filename = os.path.basename(file_path)
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
            # Get PDF metadata first
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
            page_count = len(pdf_reader.pages)
            metadata = pdf_reader.metadata or {}
            
            processed_pages = []
            
            # Try PyMuPDF first (pure Python, no external dependencies)
            if PYMUPDF_AVAILABLE:
                try:
                    pages = self._convert_pdf_with_pymupdf(file_bytes)
                    
                    # Process pages
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
                    
                    print(f"✅ PDF converted using PyMuPDF: {len(processed_pages)} pages")
                        
                except Exception as pymupdf_error:
                    print(f"PyMuPDF conversion failed: {pymupdf_error}")
                    processed_pages = []
            
            # Try pdf2image with Poppler if PyMuPDF failed
            if not processed_pages and PDF2IMAGE_AVAILABLE and self._check_poppler_installation():
                try:
                    # Convert PDF pages to images
                    pages = convert_from_bytes(
                        file_bytes,
                        dpi=200,
                        fmt='PNG'
                    )
                    
                    # Process pages
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
                    
                    print(f"✅ PDF converted using Poppler: {len(processed_pages)} pages")
                        
                except Exception as pdf_convert_error:
                    print(f"PDF conversion failed: {pdf_convert_error}")
                    processed_pages = []
            
            # Fall back to placeholder images if both methods failed
            if not processed_pages:
                processed_pages = self._create_pdf_placeholder_image(page_count, filename)
                print(f"📄 Using placeholder images: {len(processed_pages)} pages")
            
            self.document_pages = processed_pages
            self.filename = filename
            self.document_metadata = {
                'filename': filename,
                'format': 'PDF',
                'page_count': page_count,
                'metadata': self._sanitize_pdf_metadata(metadata),
                'poppler_available': PDF2IMAGE_AVAILABLE and self._check_poppler_installation()
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
            self.filename = os.path.basename(file_path)
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
            self.filename = filename
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
    
    def apply_stamps_and_export(self, stamp_overlay) -> bytes:
        """Apply stamps to the document and export as PDF bytes."""
        if not self.document_pages:
            raise ValueError("No document loaded")
        
        # Import required modules
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            from io import BytesIO
        except ImportError:
            raise ImportError("reportlab is required for PDF export. Install it with: pip install reportlab")
        
        # Create a new PDF with stamps applied
        buffer = BytesIO()
        
        # Create PDF canvas
        c = canvas.Canvas(buffer)
        
        page_count = self.get_page_count()
        for page_num in range(1, page_count + 1):
            # Get page image
            page_image = self.get_page_image(page_num)
            if not page_image:
                continue
            
            # Apply stamps to this page
            stamped_image = stamp_overlay.apply_stamps_to_image(page_image, page_num)
            
            # Convert to RGB if needed
            if stamped_image.mode != 'RGB':
                stamped_image = stamped_image.convert('RGB')
            
            # Save to buffer
            img_buffer = BytesIO()
            stamped_image.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            # Set page size based on image dimensions
            img_width, img_height = stamped_image.size
            page_width = img_width * 72 / 96  # Convert pixels to points
            page_height = img_height * 72 / 96
            
            c.setPageSize((page_width, page_height))
            c.drawInlineImage(stamped_image, 0, 0, width=page_width, height=page_height)
            
            if page_num < page_count:
                c.showPage()
        
        c.save()
        buffer.seek(0)
        return buffer.read()
    
    def get_page_image(self, page_number: int) -> Optional[Image.Image]:
        """Get PIL Image for a specific page."""
        if page_number < 1 or page_number > len(self.document_pages):
            return None
            
        page_data = self.document_pages[page_number - 1]
        
        # Try to get from base64 data
        if 'base64' in page_data:
            try:
                base64_data = page_data['base64'].split(',', 1)[1]
                image_data = base64.b64decode(base64_data)
                return Image.open(BytesIO(image_data))
            except Exception:
                pass
        
        return None