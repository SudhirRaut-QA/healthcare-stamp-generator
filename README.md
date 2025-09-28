# 🏥 Healthcare Stamp Generator

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/SudhirRaut-QA/healthcare-stamp-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/SudhirRaut-QA/healthcare-stamp-generator/actions)

A superfast and scalable healthcare application with an advanced hospital stamp generator module that creates professional circular stamps with dynamic spacing and authentic appearance.

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

### 🚀 **High Performance**
- **Dynamic precision system** prevents text overlap
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
```bash
python generate_stamp.py "Your Hospital Name"
python generate_stamp.py "City Medical Center" --size 500
```

#### 2. **Interactive Mode** (User-Friendly)
```bash
python interactive_generator.py
# Follow the prompts to enter hospital names
```

#### 3. **Web API** (Integration)
```bash
# Start the FastAPI server
uvicorn app.main:app --reload

# Access API docs at: http://localhost:8000/docs
# Generate via API: POST /api/v1/stamp/generate
```

## 📊 Dynamic Spacing Examples

The generator automatically adapts to any hospital name length:

- **Short names** (≤12 chars): Expanded spacing for balanced appearance
- **Medium names** (13-35 chars): Optimal spacing for readability  
- **Long names** (>35 chars): Compressed spacing to fit perfectly
- **Complex names** with commas/punctuation: Intelligent handling

## 🎯 Advanced Features

### **Dynamic Precision System**
- Automatic font size calculation
- Text radius optimization
- Overlap prevention algorithms
- Circular coverage optimization

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
│   ├── modules/stamp_generator/
│   │   └── generator.py          # Core stamp generation logic
│   ├── api/                      # FastAPI routes
│   ├── models/                   # Data models
│   └── main.py                   # FastAPI application
├── tests/                        # Test files
├── stampOutput/                  # Generated stamps output
├── generate_stamp.py             # Command-line generator
├── interactive_generator.py      # Interactive CLI tool
└── requirements.txt              # Dependencies
```

## 🏥 Example Output

The generator creates professional hospital stamps like:
- ● CITY MEDICAL CENTER (circular text)
- ● DR. SMITH MULTISPECIALITY HOSPITAL
- ● REGIONAL HEALTHCARE INSTITUTE

All stamps feature:
- Perfect circular text layout
- Dynamic spacing optimization
- Professional medical appearance
- Transparent background for integration

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

- `POST /api/v1/stamp/generate` - Generate a hospital stamp
- `GET /api/v1/health` - Health check endpoint

### Usage Example

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
✅ **Scalable architecture** - Handles any hospital name length  
✅ **High performance** - Optimized for production use  
✅ **Comprehensive testing** - Reliable and robust  
✅ **Easy integration** - Multiple usage options

---

**Ready for production use with any hospital name length!** 🚀