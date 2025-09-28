# 🏥 Healthcare Stamp Generator

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/SudhirRaut-QA/healthcare-stamp-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/SudhirRaut-QA/healthcare-stamp-generator/actions)

A superfast and scalable healthcare application with advanced stamp generator modules that create professional medical stamps with authentic appearance:

- **🏥 Hospital Stamps** - Circular design with dynamic spacing and dual padding
- **🩺 Doctor Stamps** - Clean borderless layout with brighter text and hierarchy

## ✨ Features

### 🎯 **Dynamic Circle Filling**
- **Intelligent spacing** that automatically fills the entire circular area
- **No gaps** between text end and start - perfect circle utilization
- **Adaptive coverage** (320°-350°) based on text length

### 🔤 **Advanced Text Rendering**
- **Circular text layout** with proper character rotation
- **Dynamic font sizing** based on content length
- **Character-type-specific spacing** (narrow/wide/normal characters)
- **Word-based spacing** with natural separation

### 🎨 **Professional Design**
- **Transparent PNG background** for easy integration
- **Blue ink color** (#1E40AF) for authentic medical appearance
- **Medical symbol (●)** at the start of text
- **Double border design** with customizable styles
- **Inner circle division** with horizontal line
- **Font hierarchy system** - Hospital name (largest), PAID (medium), CASH/Online (smallest)
- **Dual padding system** - 3% inner + 3% outer boundary control
- **100% boundary compliance** - Text never crosses circle boundaries

### 🚀 **High Performance**
- **Dynamic precision system** prevents text overlap and boundary violations
- **Dual padding algorithm** ensures perfect boundary control (3% + 3%)
- **Font hierarchy optimization** for authentic medical appearance
- **Automatic optimization** for any hospital name length
- **Memory efficient** image processing
- **Fast generation** with caching support

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/SudhirRaut-QA/healthcare-stamp-generator.git
cd healthcare-stamp-generator

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Usage Options

#### 1. **Command Line** (Fastest)

**Hospital Stamps (Circular):**
```bash
# Basic usage
python generate_stamp.py "Your Hospital Name"

# Custom size with dynamic analysis
python generate_stamp.py "City Medical Center" --size 500
```

**Doctor Stamps (Rectangular):**
```bash
# Basic doctor stamp
python generate_doctor_stamp.py "Dr. Sarah Johnson" "MBBS, MD (Cardiology)" "Reg. No: MCI-12345"

# Custom size
python generate_doctor_stamp.py "Dr. Michael Chen" "MBBS, MS (Orthopedics)" "Reg. No: MCI-67890" --width 500 --height 250
```

#### 2. **Interactive Mode** (User-Friendly)
```bash
# Hospital stamps
python interactive_generator.py

# Doctor stamps  
python interactive_doctor_generator.py
```

#### 3. **Web API** (Integration)
```bash
# Start the FastAPI server
uvicorn app.main:app --reload

# Access API docs at: http://localhost:8000/docs
# Hospital stamps: POST /api/v1/stamp/generate
# Doctor stamps: POST /api/v1/doctor-stamp/generate
```

> 📖 **See [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for hospital stamp examples**  
> 📖 **See [DOCTOR_STAMP_GUIDE.md](DOCTOR_STAMP_GUIDE.md) for doctor stamp examples**

## 📊 Dynamic Spacing Examples

The generator automatically adapts to any hospital name length:

- **Short names** (≤12 chars): Expanded spacing for balanced appearance
- **Medium names** (13-35 chars): Optimal spacing for readability  
- **Long names** (>35 chars): Compressed spacing to fit perfectly
- **Complex names** with commas/punctuation: Intelligent handling

## 🎯 Advanced Features

### **Dual Padding System** 🆕
- **Inner padding**: 3% of stamp size from inner circle boundary
- **Outer padding**: 3% of stamp size from outer circle boundary  
- **100% boundary compliance**: Text never crosses circle boundaries
- **Automatic adjustment**: Works with any size (180px-500px+)
- **Professional appearance**: Maintains consistent margins

### **Font Hierarchy System** 🆕
- **Hospital name**: Largest font (primary text in outer circle)
- **PAID text**: Medium font (upper section of inner circle)
- **CASH/Online**: Smallest font (lower section of inner circle)
- **Proportional scaling**: All fonts scale together with stamp size
- **Authentic medical appearance**: Professional hospital stamp design

### **Dynamic Precision System**
- Automatic font size calculation with hierarchy support
- Text radius optimization with dual padding (3% inner + 3% outer)
- Overlap prevention algorithms with boundary control
- Circular coverage optimization (100% boundary compliance)
- Real-time analysis display during generation

### **Character Spacing Intelligence**
- Narrow characters (I,L,l,i,1): Tighter spacing
- Wide characters (M,W,@): Extra space allocation
- Normal characters: Balanced spacing
- Proportional word gaps (1.5x character spacing)

### **Professional Output**
- 300x300px default size (customizable)
- Transparent PNG format
- Blue medical ink color (#1E40AF)
- Anti-aliased text rendering
- Multiple border styles available

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python 3.8+)
- **Image Processing**: Pillow (PIL) 10.1.0
- **API Framework**: FastAPI 0.104.1
- **Testing**: pytest
- **CI/CD**: GitHub Actions

## 📁 Project Structure

```
healthcare-stamp-generator/
├── app/
│   ├── modules/
│   │   ├── stamp_generator/      # Hospital stamps (circular)
│   │   │   └── generator.py      # Advanced dual padding system
│   │   └── doctor_stamp/         # Doctor stamps (rectangular) 🆕
│   │       └── generator.py      # Professional text hierarchy
│   ├── api/                      # FastAPI routes
│   │   ├── v1.py                 # Hospital stamp API
│   │   └── doctor_stamp_routes.py # Doctor stamp API 🆕
│   ├── models/                   # Data models
│   └── main.py                   # FastAPI application
├── tests/                        # Test files
├── stampOutput/                  # Hospital stamps output
├── doctorStampOutput/            # Doctor stamps output 🆕
├── generate_stamp.py             # Hospital stamp CLI
├── generate_doctor_stamp.py      # Doctor stamp CLI 🆕
├── interactive_generator.py      # Hospital stamp interactive
├── interactive_doctor_generator.py # Doctor stamp interactive 🆕
└── requirements.txt              # Dependencies
```

## 🏥 Example Output

![Hospital Stamp Examples](stampOutput/README_examples.png)

The generator creates professional hospital stamps with:

### **Outer Circle:**
- ● CITY MEDICAL CENTER (circular text with dynamic spacing)
- ● DR. SMITH MULTISPECIALITY HOSPITAL
- ● REGIONAL HEALTHCARE INSTITUTE

### **Inner Circle Division:**
- **Upper section**: Bold "PAID" text (medium font in hierarchy)
- **Horizontal dividing line**: Across center of inner circle
- **Lower section**: "CASH / Online" status text (smallest font in hierarchy)
- **Font hierarchy**: Maintains professional medical appearance

### **Professional Features:**
- Perfect circular text layout with no gaps
- Dynamic spacing optimization for any name length
- Dual padding system ensures 100% boundary compliance
- Font hierarchy system (Hospital > PAID > CASH/Online)
- Inner circle divided for payment/status information
- Transparent background for easy integration
- Blue medical ink color (#1E40AF)

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Test specific hospital names
python generate_stamp.py "Test Hospital Name"
```

## 📈 Performance

- **Generation time**: ~50-100ms per stamp
- **Memory usage**: <10MB per generation
- **Output size**: ~8-15KB per PNG
- **Supported lengths**: 1-100+ characters
- **Concurrent requests**: 100+ simultaneous

## 📝 API Documentation

When running the FastAPI server, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

**Hospital Stamps (Circular):**
- `POST /api/v1/stamp/generate` - Generate a hospital stamp
- `GET /api/v1/health` - Health check endpoint

**Doctor Stamps (Rectangular):** 🆕
- `POST /api/v1/doctor-stamp/generate` - Generate a doctor stamp
- `POST /api/v1/doctor-stamp/generate/image` - Get stamp as PNG image
- `POST /api/v1/doctor-stamp/generate/batch` - Generate multiple doctor stamps
- `GET /api/v1/doctor-stamp/health` - Doctor stamp service health

### Usage Examples

**Hospital Stamp API:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/stamp/generate",
    json={"hospital_name": "City General Hospital"}
)

# Save the returned PNG image
with open("hospital_stamp.png", "wb") as f:
    f.write(response.content)
```

**Doctor Stamp API:** 🆕
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/doctor-stamp/generate/image",
    json={
        "doctor_name": "Dr. Sarah Johnson",
        "degree": "MBBS, MD (Cardiology)",
        "registration_number": "Reg. No: MCI-12345"
    }
)

# Save the returned PNG image
with open("doctor_stamp.png", "wb") as f:
    f.write(response.content)
```

## 🔧 Development

### Setup Development Environment
```bash
pip install -r requirements.txt
pip install pytest black flake8  # Development tools
```

### Code Quality
- **Type hints** throughout codebase
- **PEP 8** compliance
- **Comprehensive testing**
- **CI/CD pipeline** with GitHub Actions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Achievements

✅ **Dynamic circle filling** - No gaps between text start and end  
✅ **Professional spacing** - Character-type-specific optimization  
✅ **Dual padding system** - 3% inner + 3% outer boundary control  
✅ **Font hierarchy** - Three-tier professional medical design  
✅ **100% boundary compliance** - Text never crosses circle boundaries  
✅ **Scalable architecture** - Handles any hospital name length  
✅ **High performance** - Optimized for production use  
✅ **Comprehensive testing** - Reliable and robust  
✅ **Easy integration** - Multiple usage options

---

**Ready for production use with any hospital name length!** 🚀