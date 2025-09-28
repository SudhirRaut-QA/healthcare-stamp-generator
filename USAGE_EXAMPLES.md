# 🏥 Usage Examples - Healthcare Stamp Generator

## Advanced Features Showcase

### 1. Dual Padding System
The dual padding system ensures perfect boundary control with 3% inner + 3% outer padding:

```bash
# Small stamp - padding scales proportionally
python generate_stamp.py "ABC Hospital" --size 200

# Large stamp - maintains boundary control
python generate_stamp.py "Metropolitan General Hospital" --size 500
```

### 2. Font Hierarchy System
Three-tier font hierarchy creates professional medical appearance:

- **Hospital Name**: Largest font (outer circle)
- **PAID**: Medium font (inner circle upper)
- **CASH/Online**: Smallest font (inner circle lower)

### 3. Dynamic Analysis Output
Real-time feedback shows optimization details:

```
🏥 Generating stamp for: Regional Healthcare Institute
📏 Size: 350x350 pixels
🔧 Dynamic Analysis:
   • Font size: 26px (auto-optimized)
   • Text radius: 110px (dual padding applied)
   • Character spacing: 9.9° (no overlap)
   • Gap width: 41px
✅ Stamp generated successfully!
```

### 4. Boundary Compliance Testing
Test various lengths to see 100% boundary compliance:

```bash
# Short name
python generate_stamp.py "ABC"

# Medium name  
python generate_stamp.py "City Medical Center"

# Long name
python generate_stamp.py "Dr. Smith Memorial Multispecialty Healthcare Institute"

# All maintain perfect boundary control!
```

### 5. Multiple Size Testing
Works flawlessly across all sizes:

```bash
python generate_stamp.py "General Hospital" --size 180
python generate_stamp.py "General Hospital" --size 300  
python generate_stamp.py "General Hospital" --size 400
python generate_stamp.py "General Hospital" --size 500
```

## Expected Output Files

Generated stamps are saved to `stampOutput/` folder:
- `stamp_abc_hospital.png` 
- `stamp_city_medical_center.png`
- `stamp_general_hospital.png`
- `stamp_regional_healthcare_institute.png`

Each stamp features:
✅ Transparent PNG background  
✅ Blue medical ink color (#1E40AF)  
✅ Perfect circular text layout  
✅ Dual padding boundary control  
✅ Font hierarchy system  
✅ Inner circle with PAID/CASH sections  

## Professional Features

- **Zero boundary violations** - Text never crosses circle lines
- **Authentic medical appearance** - Professional hospital stamp design  
- **Scalable to any size** - 180px to 500px+ supported
- **Dynamic optimization** - Automatic spacing and font sizing
- **Production ready** - Used in healthcare applications

Ready for professional healthcare use! 🚀