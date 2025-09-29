# 📄 Document Stamping System Guide

## 🎯 Overview

The Healthcare Document Stamping System provides an advanced solution for adding professional stamps to healthcare documents such as prescriptions, invoices, and medical records. The system supports both interactive web-based stamping and command-line operations.

## ✨ Key Features

### 🖱️ **Interactive Web Interface**
- **Drag & Drop Upload**: Support for PDF and image files
- **Click-to-Place**: Click anywhere on the document to position stamps
- **Real-time Preview**: See stamps as you add them
- **Multi-page Support**: Navigate through PDF pages
- **Stamp Management**: Move, resize, delete, and configure stamps
- **Export Options**: Download stamped documents and configurations

### 🔖 **Dual Stamp System**
- **Hospital Stamps**: Circular design with dynamic text spacing
- **Doctor Stamps**: Rectangular layout with auto-prefix registration numbers

### 🛠️ **Advanced Features**
- **Stamp Manipulation**: Drag to move, resize handles, rotation, opacity control
- **Boundary Display**: Show stamp boundaries for precise editing
- **Configuration Export/Import**: Save and load stamp configurations
- **Session Management**: Multiple concurrent stamping sessions
- **CLI Support**: Command-line interface for automation

## 🚀 Getting Started

### **1. Installation**

First, install the additional dependencies for document processing:

```bash
# Install document processing dependencies
pip install pdf2image PyPDF2 aiofiles

# For PDF processing, you may also need poppler (system dependency)
# Windows: Download from https://github.com/oschwartz10612/poppler-windows
# macOS: brew install poppler
# Ubuntu/Debian: sudo apt-get install poppler-utils
```

### **2. Start the Application**

```bash
# Start the FastAPI server
uvicorn app.main:app --reload --port 8000

# The application will be available at:
# http://localhost:8000 - Main interface
# http://localhost:8000/static/document_stamper.html - Document Stamper
# http://localhost:8000/docs - API Documentation
```

## 🖥️ Web Interface Usage

### **Step 1: Upload Document**
1. Open the Document Stamper interface
2. Drag & drop your document or click to browse
3. Supported formats: PDF, PNG, JPG, JPEG, BMP, TIFF
4. Maximum file size: 50MB

### **Step 2: Add Stamps**
1. Click "🏥 Hospital Stamp" or "🩺 Doctor Stamp"
2. Fill in the required information:
   - **Hospital Stamp**: Hospital name
   - **Doctor Stamp**: Doctor name, degree, registration number
3. Click anywhere on the document preview to place the stamp

### **Step 3: Manage Stamps**
- **Move**: Click and drag stamps to new positions
- **Delete**: Use the delete button in the stamps list
- **Toggle Boundaries**: Show/hide stamp boundaries for editing
- **Clear All**: Remove all stamps from the document

### **Step 4: Navigate Pages**
- For multi-page PDFs, use the page navigation controls
- Each page can have different stamps
- Preview updates automatically when changing pages

### **Step 5: Export & Save**
- **Download**: Save the stamped document as PDF/PNG
- **Export Config**: Save stamp configuration for reuse
- **Import Config**: Load previously saved stamp configurations

## 💻 Command Line Interface

### **Basic Usage**

```bash
# Interactive mode with document
python document_stamper_cli.py prescription.pdf --interactive

# Add hospital stamp and save
python document_stamper_cli.py invoice.pdf --hospital "General Hospital" --save stamped_invoice.pdf

# Add doctor stamp with custom position
python document_stamper_cli.py prescription.pdf \
  --doctor "Dr. Sarah Johnson" \
  --degree "MBBS, MD" \
  --registration "MCI-12345" \
  --position "0.8,0.2" \
  --save
```

### **Interactive Commands**

When running in interactive mode:

```bash
# Document information
info

# Add stamps
hospital 1 "City General Hospital"
doctor  # (prompts for details)

# Preview and save
preview 1
save

# Manage stamps
list        # List all stamps
list 1      # List stamps on page 1
clear 1     # Clear stamps from page 1
clear       # Clear all stamps

# Help
help
quit
```

## 🌐 REST API Usage

### **Create Session**

```bash
curl -X POST "http://localhost:8000/api/v1/document-stamper/session/create"
```

### **Upload Document**

```bash
curl -X POST "http://localhost:8000/api/v1/document-stamper/document/upload" \
  -F "session_id=your-session-id" \
  -F "file=@prescription.pdf"
```

### **Add Hospital Stamp**

```bash
curl -X POST "http://localhost:8000/api/v1/document-stamper/stamp/add" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "page_number": 1,
    "stamp_type": "hospital",
    "hospital_name": "General Hospital",
    "x": 0.5,
    "y": 0.3
  }'
```

### **Add Doctor Stamp**

```bash
curl -X POST "http://localhost:8000/api/v1/document-stamper/stamp/add" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "page_number": 1,
    "stamp_type": "doctor",
    "doctor_name": "Dr. Sarah Johnson",
    "degree": "MBBS, MD (Cardiology)",
    "registration_number": "MCI-12345",
    "x": 0.8,
    "y": 0.2
  }'
```

### **Generate Preview**

```bash
curl -X POST "http://localhost:8000/api/v1/document-stamper/preview/page" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "page_number": 1,
    "preview_width": 800,
    "show_boundaries": false
  }'
```

## 🎨 Stamp Positioning System

### **Coordinate System**
- **X-axis**: 0.0 (left edge) to 1.0 (right edge)
- **Y-axis**: 0.0 (top edge) to 1.0 (bottom edge)
- **Center**: (0.5, 0.5)

### **Common Positions**
```json
{
  "top_left": {"x": 0.1, "y": 0.1},
  "top_right": {"x": 0.9, "y": 0.1},
  "center": {"x": 0.5, "y": 0.5},
  "bottom_left": {"x": 0.1, "y": 0.9},
  "bottom_right": {"x": 0.9, "y": 0.9}
}
```

## 🔧 Advanced Configuration

### **Stamp Properties**
Each stamp can be configured with:
- **Position**: X, Y coordinates (0.0-1.0)
- **Size**: Width and height in pixels (50-800)
- **Rotation**: Angle in degrees (0-359)
- **Opacity**: Transparency level (0.0-1.0)
- **Z-Index**: Layer order for overlapping stamps

### **Document Processing Settings**
- **Maximum file size**: 50MB
- **Maximum image dimension**: 4000px
- **Supported formats**: PDF, PNG, JPG, JPEG, BMP, TIFF, GIF
- **Preview DPI**: 200 (high quality)

## 📊 Performance Optimization

### **Best Practices**
- Use appropriate preview sizes (800px width recommended)
- Limit stamp count per page (< 10 for optimal performance)
- Process pages individually for large documents
- Enable boundary display only when editing

### **Memory Management**
- Sessions are automatically cleaned up
- Large images are automatically resized
- Preview images are optimized for web display

## 🛡️ Error Handling

### **Common Issues**
1. **PDF Processing Errors**: Install poppler system dependency
2. **Large File Upload**: Check file size limits (50MB max)
3. **Session Not Found**: Create a new session
4. **Invalid Coordinates**: Use values between 0.0 and 1.0

### **Troubleshooting**
```bash
# Check system dependencies
python -c "import pdf2image; print('PDF2Image: OK')"
python -c "import PyPDF2; print('PyPDF2: OK')"

# Test with sample document
curl -X POST "http://localhost:8000/api/v1/document-stamper/session/create"

# Check logs for detailed error information
uvicorn app.main:app --log-level debug
```

## 🔗 Integration Examples

### **Python Integration**

```python
import requests
import json

# Create session
session_response = requests.post("http://localhost:8000/api/v1/document-stamper/session/create")
session_id = session_response.json()["session_id"]

# Upload document
with open("prescription.pdf", "rb") as f:
    files = {"file": f}
    data = {"session_id": session_id}
    upload_response = requests.post(
        "http://localhost:8000/api/v1/document-stamper/document/upload",
        files=files,
        data=data
    )

# Add stamp
stamp_data = {
    "session_id": session_id,
    "page_number": 1,
    "stamp_type": "hospital",
    "hospital_name": "General Hospital",
    "x": 0.5,
    "y": 0.3
}
stamp_response = requests.post(
    "http://localhost:8000/api/v1/document-stamper/stamp/add",
    json=stamp_data
)

print("Stamp added:", stamp_response.json())
```

### **JavaScript Integration**

```javascript
// Create session
const sessionResponse = await fetch('/api/v1/document-stamper/session/create', {
    method: 'POST'
});
const { session_id } = await sessionResponse.json();

// Upload document
const formData = new FormData();
formData.append('session_id', session_id);
formData.append('file', fileInput.files[0]);

const uploadResponse = await fetch('/api/v1/document-stamper/document/upload', {
    method: 'POST',
    body: formData
});

// Add stamp
const stampData = {
    session_id: session_id,
    page_number: 1,
    stamp_type: 'doctor',
    doctor_name: 'Dr. Smith',
    degree: 'MBBS',
    registration_number: 'MCI-123',
    x: 0.8,
    y: 0.2
};

const stampResponse = await fetch('/api/v1/document-stamper/stamp/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(stampData)
});
```

## 🎯 Use Cases

### **Healthcare Workflows**
1. **Prescription Stamping**: Add doctor stamps to prescriptions
2. **Invoice Processing**: Stamp hospital invoices with official stamps
3. **Medical Records**: Add verification stamps to patient records
4. **Certificate Validation**: Stamp medical certificates
5. **Report Authorization**: Add doctor signatures to reports

### **Batch Processing**
```bash
# Process multiple documents
for file in prescriptions/*.pdf; do
    python document_stamper_cli.py "$file" \
        --hospital "City Hospital" \
        --save "stamped_$(basename "$file")"
done
```

## 📚 API Reference

### **Session Management**
- `POST /api/v1/document-stamper/session/create` - Create session
- `DELETE /api/v1/document-stamper/session/{session_id}` - Delete session
- `GET /api/v1/document-stamper/sessions/list` - List active sessions

### **Document Operations**
- `POST /api/v1/document-stamper/document/upload` - Upload document
- `GET /api/v1/document-stamper/document/{session_id}/info` - Get document info

### **Stamp Operations**
- `POST /api/v1/document-stamper/stamp/add` - Add stamp
- `PUT /api/v1/document-stamper/stamp/move` - Move stamp
- `PUT /api/v1/document-stamper/stamp/resize` - Resize stamp
- `PUT /api/v1/document-stamper/stamp/rotate` - Rotate stamp
- `PUT /api/v1/document-stamper/stamp/opacity` - Set opacity
- `DELETE /api/v1/document-stamper/stamp/delete` - Delete stamp

### **Preview & Export**
- `POST /api/v1/document-stamper/preview/page` - Generate preview
- `GET /api/v1/document-stamper/preview/page/{session_id}/{page_number}/image` - Get preview image
- `GET /api/v1/document-stamper/stamps/{session_id}/export` - Export configuration
- `POST /api/v1/document-stamper/stamps/{session_id}/import` - Import configuration

---

## 🎉 Ready for Professional Document Stamping!

The Document Stamping System provides a complete solution for healthcare document processing with:

- ✅ **Interactive Web Interface** with drag & drop functionality
- ✅ **Professional Stamp Generation** with hospital and doctor stamps
- ✅ **Advanced Positioning System** with click-to-place and drag-to-move
- ✅ **Multi-format Support** for PDF and image documents
- ✅ **Real-time Preview** with boundary display and editing
- ✅ **CLI Tools** for automation and batch processing
- ✅ **Complete REST API** for integration with other systems
- ✅ **Session Management** for concurrent users
- ✅ **Export/Import** functionality for stamp configurations

**Start stamping your healthcare documents today!** 🚀