# 🏥 Healthcare Operations Application

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A superfast and scalable healthcare application with hospital stamp generator functionality. Generate professional circular hospital stamps with transparent backgrounds, perfect for prescription printing.

## Features

- **Hospital Stamp Generator**: Generate circular hospital stamps with custom names
- **PNG Output**: Transparent background stamps for prescription printing
- **Blue Ink Style**: Professional medical stamp appearance
- **Scalable API**: Built with FastAPI for high performance

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn app.main:app --reload
```

3. Access the API documentation:
```
http://localhost:8000/docs
```

## API Endpoints

- `POST /api/v1/stamp/generate` - Generate a hospital stamp
- `GET /api/v1/health` - Health check endpoint

## Usage Example

Generate a hospital stamp:
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

## Technology Stack

- **FastAPI**: High-performance web framework
- **Pillow (PIL)**: Image processing library
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

## Development

The application follows a modular architecture:
- `app/modules/stamp_generator/` - Core stamp generation logic
- `app/api/` - API route handlers
- `app/models/` - Pydantic models
- `tests/` - Unit and integration tests

## 📋 Requirements

- Python 3.8+
- See `requirements.txt` for detailed dependencies

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) for high-performance web APIs
- Image processing powered by [Pillow](https://python-pillow.org/)
- Testing with [pytest](https://pytest.org/)

## 📞 Support

For support, please open an issue on GitHub or contact the maintainers.