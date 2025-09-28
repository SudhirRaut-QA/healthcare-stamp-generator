# 🩺 Doctor Stamp Generator - Usage Guide

## Overview
The Doctor Stamp Generator creates professional rectangular stamps for medical professionals with authentic appearance and proper hierarchy.

## Features
- **Clean rectangular layout** - Minimalist, medical-grade appearance
- **Three-tier text hierarchy** - Name > Degree > Registration
- **Auto-prefix for registration** - "Reg. No.:" prefix automatically added if not present
- **Scalable sizing** - Proportional fonts across all sizes (200x100 to 800x400)
- **Borderless design** - Clean, modern appearance
- **Vibrant bright text** - Maximum visibility with bright blue (#0066FF for text, #0080FF for names)
- **Realistic medical fonts** - Times New Roman priority for authentic appearance
- **Enhanced visibility** - Doctor names get subtle shadows for prominence
- **Transparent background** - Easy integration into documents

## 🆕 New Feature: Auto-Prefix Registration Numbers
You can now provide just the registration number (e.g., `"MCI-12345"`) and the system will automatically add the `"Reg. No.: "` prefix. This makes the API more flexible while maintaining consistent formatting.

## Usage Options

### 1. Command Line Interface
```bash
# Basic usage
python generate_doctor_stamp.py "Dr. Sarah Johnson" "MBBS, MD (Cardiology)" "Reg. No: MCI-12345"

# Custom size
python generate_doctor_stamp.py "Dr. Michael Chen" "MBBS, MS (Orthopedics)" "Reg. No: MCI-67890" --width 500 --height 250

# Custom output path
python generate_doctor_stamp.py "Dr. Priya Sharma" "MBBS, DGO" "Reg. No: MCI-11223" --output "custom_stamp.png"
```

### 2. Interactive Mode
```bash
python interactive_doctor_generator.py
```
Follow the prompts to enter doctor details interactively.

### 3. Python API
```python
from app.modules.doctor_stamp.generator import DoctorStampGenerator

generator = DoctorStampGenerator()

# Generate single stamp
stamp_path = generator.generate_doctor_stamp(
    doctor_name="Dr. Sarah Johnson",
    degree="MBBS, MD (Cardiology)",
    registration_number="MCI-12345",  # 'Reg. No.:' prefix auto-added
    width=400,
    height=200
)

# Generate batch stamps
doctors_data = [
    {
        "name": "Dr. Sarah Johnson",
        "degree": "MBBS, MD (Cardiology)",
        "registration": "MCI-12345"
    },
    {
        "name": "Dr. Michael Chen", 
        "degree": "MBBS, MS (Orthopedics)",
        "registration": "MCI-67890"
    }
]

generated_files = generator.generate_batch_stamps(doctors_data)
```

### 4. REST API Endpoints

#### Generate Single Doctor Stamp
```bash
POST /api/v1/doctor-stamp/generate
Content-Type: application/json

{
    "doctor_name": "Dr. Sarah Johnson",
    "degree": "MBBS, MD (Cardiology)",
    "registration_number": "MCI-12345",  // 'Reg. No.:' prefix auto-added
    "width": 400,
    "height": 200
}
```

#### Get Stamp as Image
```bash
POST /api/v1/doctor-stamp/generate/image
Content-Type: application/json

{
    "doctor_name": "Dr. Sarah Johnson",
    "degree": "MBBS, MD (Cardiology)",
    "registration_number": "Reg. No: MCI-12345"
}
```

#### Batch Generation
```bash
POST /api/v1/doctor-stamp/generate/batch
Content-Type: application/json

{
    "doctors": [
        {
            "doctor_name": "Dr. Sarah Johnson",
            "degree": "MBBS, MD (Cardiology)",
            "registration_number": "MCI-12345"
        },
        {
            "doctor_name": "Dr. Michael Chen",
            "degree": "MBBS, MS (Orthopedics)", 
            "registration_number": "MCI-67890"
        }
    ]
}
```

## Text Hierarchy

### 1. Doctor Name (Top Line)
- **Font**: Bold, largest size
- **Position**: Top center
- **Auto-sizing**: Based on stamp width (width ÷ 16)
- **Examples**: "Dr. Sarah Johnson", "Dr. Michael Chen"

### 2. Medical Degree (Middle)
- **Font**: Regular weight, medium size  
- **Position**: Center, below name
- **Auto-sizing**: Based on stamp width (width ÷ 25)
- **Examples**: "MBBS, MD (Cardiology)", "MBBS, MS (Orthopedics)"

### 3. Registration Number (Bottom)
- **Font**: Regular weight, smallest size
- **Position**: Bottom center
- **Auto-sizing**: Based on stamp width (width ÷ 33)
- **Examples**: "Reg. No: MCI-12345", "Reg. No: MCI-67890"

## Size Guidelines

### Standard Sizes
- **Small**: 300x150 pixels - Compact stamps
- **Medium**: 400x200 pixels - Standard professional size
- **Large**: 500x250 pixels - For detailed information
- **Extra Large**: 600x300 pixels - Maximum readability

### Size Constraints
- **Width**: 200-800 pixels
- **Height**: 100-400 pixels
- **Aspect Ratio**: Recommended 2:1 (width:height)

## Professional Examples

### Cardiologist
```
Dr. Sarah Johnson
MBBS, MD (Cardiology)
Reg. No: MCI-12345
```

### Orthopedic Surgeon
```
Dr. Michael Chen
MBBS, MS (Orthopedics)
Reg. No: MCI-67890
```

### Gynecologist
```
Dr. Priya Sharma
MBBS, DGO, MD (Gynecology & Obstetrics)
Reg. No: MCI-11223
```

## Output Files

### File Naming Convention
- Generated files use safe naming: `doctor_stamp_[safe_doctor_name].png`
- Special characters are replaced with underscores
- All lowercase for consistency

### File Location
- Default: `doctorStampOutput/` folder
- Custom paths supported via `--output` parameter
- Automatic directory creation

### File Format
- **Format**: PNG with transparency
- **Background**: Transparent (RGBA)
- **Colors**: Vibrant blue (#0066FF/#0080FF) on transparent for maximum visibility
- **Fonts**: Realistic medical fonts with Times New Roman priority
- **Enhancement**: Subtle shadows on names for depth and prominence
- **Size**: Typically 7-18KB per stamp (slightly larger due to font enhancements)

## Advanced Features

### Text Wrapping
- Automatic text wrapping for long names/degrees
- Intelligent word breaks
- Maintains professional appearance

### Font Fallback System
- Primary: Calibri (Windows)
- Secondary: Arial (Cross-platform)
- Tertiary: Times (Classic)
- Fallback: System default

### Design Style
- **Layout**: Clean borderless rectangular design
- **Text Colors**: 
  - Doctor names: Extra bright blue (#0080FF) with shadow
  - Degrees & Registration: Vibrant blue (#0066FF)
- **Typography**: Realistic medical fonts (Times New Roman, Georgia, Calibri)
- **Enhancement**: Subtle shadows on doctor names for prominence
- **Background**: Fully transparent for seamless integration
- **Style**: Modern professional with authentic medical appearance

## Integration Examples

### Healthcare Management System
```python
# Generate stamps for all doctors in hospital
doctors = get_doctors_from_database()
generator = DoctorStampGenerator()

for doctor in doctors:
    stamp_path = generator.generate_doctor_stamp(
        doctor_name=f"Dr. {doctor.name}",
        degree=doctor.qualifications,
        registration_number=f"Reg. No: {doctor.registration}"
    )
    doctor.stamp_path = stamp_path
    doctor.save()
```

### Document Processing
```python
from PIL import Image

# Load document and doctor stamp
document = Image.open("prescription.png")
stamp = Image.open("doctor_stamp_dr_sarah_johnson.png")

# Overlay stamp on document
document.paste(stamp, (document.width - stamp.width - 50, 50), stamp)
document.save("signed_prescription.png")
```

## Testing & Validation

### Size Testing
Test across all supported sizes to ensure proper scaling:
```bash
python generate_doctor_stamp.py "Dr. Test" "MBBS" "Reg. No: 123" --width 200 --height 100
python generate_doctor_stamp.py "Dr. Test" "MBBS" "Reg. No: 123" --width 400 --height 200  
python generate_doctor_stamp.py "Dr. Test" "MBBS" "Reg. No: 123" --width 600 --height 300
```

### Text Length Testing  
Test with various text lengths:
```bash
# Short name
python generate_doctor_stamp.py "Dr. Lee" "MBBS" "Reg. No: 123"

# Long name
python generate_doctor_stamp.py "Dr. Christopher Alexander" "MBBS, MD, PhD" "Reg. No: 123456"

# Very long degree
python generate_doctor_stamp.py "Dr. Smith" "MBBS, MD (Internal Medicine), DM (Cardiology), FACC" "Reg. No: 123"
```

## Best Practices

1. **Consistent Format**: Always use "Dr." prefix for names
2. **Standard Registration**: The "Reg. No.:" prefix is automatically added - just provide the registration number (e.g., "MCI-12345")
3. **Degree Abbreviations**: Use standard medical abbreviations (MBBS, MD, MS, etc.)
4. **Size Selection**: Use 400x200 for most applications
5. **File Management**: Organize stamps by department or date
6. **Quality Check**: Verify text readability before use

## Troubleshooting

### Common Issues

**Issue**: Text appears cut off
**Solution**: Increase stamp height or reduce text length

**Issue**: Font appears too small
**Solution**: Increase stamp width (fonts scale with width)

**Issue**: Registration number missing
**Solution**: Ensure registration_number parameter is provided

**Issue**: Output folder not found
**Solution**: Generator automatically creates `doctorStampOutput/` folder

### Error Messages

- `"Doctor name, degree, and registration number are required"` - All three parameters must be provided
- `"Width must be between 200 and 800 pixels"` - Width outside supported range
- `"Height must be between 100 and 400 pixels"` - Height outside supported range

## Professional Medical Standards

### Information Hierarchy
1. **Doctor Name**: Most prominent (identity)
2. **Qualifications**: Secondary (credentials)  
3. **Registration**: Tertiary (legal requirement)

### Visual Standards
- **Professional blue color** (#1E40AF) - Standard medical documentation color
- **Clean typography** - Easy to read and photocopy
- **Proper spacing** - Balanced layout with adequate margins
- **Border design** - Professional appearance with double borders

Ready for professional healthcare use! 🩺✨