#!/usr/bin/env python3
"""
Create a sample prescription for testing the document stamping system.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_prescription():
    """Create a sample prescription document for testing."""
    
    # Create image (A4 size at 200 DPI: 1654x2339)
    width, height = 1200, 1600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to use a professional font
    try:
        # Try common system fonts
        title_font = ImageFont.truetype("arial.ttf", 28)
        header_font = ImageFont.truetype("arial.ttf", 16)
        content_font = ImageFont.truetype("arial.ttf", 14)
    except:
        try:
            title_font = ImageFont.truetype("calibri.ttf", 28)
            header_font = ImageFont.truetype("calibri.ttf", 16)
            content_font = ImageFont.truetype("calibri.ttf", 14)
        except:
            # Fallback to default font
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            content_font = ImageFont.load_default()
    
    # Colors
    blue_color = (0, 102, 255)
    black_color = (0, 0, 0)
    gray_color = (100, 100, 100)
    
    # Header section
    draw.rectangle([50, 50, width-50, 150], outline=blue_color, width=3)
    draw.text((70, 70), "CITY GENERAL HOSPITAL", fill=blue_color, font=title_font)
    draw.text((70, 105), "123 Healthcare Drive, Medical City, MC 12345", fill=gray_color, font=header_font)
    draw.text((70, 125), "Phone: (555) 123-4567 | Email: info@citygeneral.com", fill=gray_color, font=header_font)
    
    # Prescription header
    draw.text((70, 180), "PRESCRIPTION", fill=black_color, font=title_font)
    draw.line([70, 210, width-70, 210], fill=blue_color, width=2)
    
    # Patient information
    y_pos = 240
    draw.text((70, y_pos), "Patient Information:", fill=blue_color, font=header_font)
    y_pos += 30
    draw.text((70, y_pos), "Name: John Smith", fill=black_color, font=content_font)
    y_pos += 25
    draw.text((70, y_pos), "Age: 45 years", fill=black_color, font=content_font)
    y_pos += 25
    draw.text((70, y_pos), "Gender: Male", fill=black_color, font=content_font)
    y_pos += 25
    draw.text((70, y_pos), "Date: September 29, 2025", fill=black_color, font=content_font)
    
    # Prescription details
    y_pos += 50
    draw.text((70, y_pos), "Prescription Details:", fill=blue_color, font=header_font)
    y_pos += 30
    
    medications = [
        "1. Amoxicillin 500mg - Take 1 tablet twice daily for 7 days",
        "2. Paracetamol 650mg - Take 1 tablet as needed for pain (max 4/day)",
        "3. Vitamin D3 1000 IU - Take 1 tablet daily with food",
        "4. Omeprazole 20mg - Take 1 tablet before breakfast for 14 days"
    ]
    
    for med in medications:
        draw.text((70, y_pos), med, fill=black_color, font=content_font)
        y_pos += 30
    
    # Instructions
    y_pos += 30
    draw.text((70, y_pos), "Instructions:", fill=blue_color, font=header_font)
    y_pos += 30
    instructions = [
        "• Take medications as prescribed",
        "• Complete the full course of antibiotics",
        "• Return for follow-up in 2 weeks",
        "• Contact doctor if symptoms worsen"
    ]
    
    for instruction in instructions:
        draw.text((70, y_pos), instruction, fill=black_color, font=content_font)
        y_pos += 25
    
    # Doctor signature area
    y_pos += 80
    draw.rectangle([width-400, y_pos, width-70, y_pos+120], outline=gray_color, width=1)
    draw.text((width-390, y_pos+10), "Doctor's Stamp & Signature", fill=gray_color, font=header_font)
    draw.text((width-390, y_pos+40), "Dr. Sarah Johnson", fill=black_color, font=content_font)
    draw.text((width-390, y_pos+60), "MBBS, MD (Internal Medicine)", fill=black_color, font=content_font)
    draw.text((width-390, y_pos+80), "Reg. No.: MCI-67890", fill=black_color, font=content_font)
    
    # Hospital stamp area
    draw.rectangle([70, y_pos, 280, y_pos+120], outline=gray_color, width=1)
    draw.text((80, y_pos+10), "Hospital Official Stamp", fill=gray_color, font=header_font)
    
    # Footer
    y_pos += 160
    draw.text((70, y_pos), "This is a computer-generated prescription.", fill=gray_color, font=content_font)
    draw.text((70, y_pos+20), "For any queries, please contact the hospital.", fill=gray_color, font=content_font)
    
    return image

def main():
    """Create sample prescription and save it."""
    print("🏥 Creating sample prescription for document stamping tests...")
    
    # Create output directory
    output_dir = "sampleDocuments"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create prescription
    prescription = create_sample_prescription()
    
    # Save as PNG
    png_path = os.path.join(output_dir, "sample_prescription.png")
    prescription.save(png_path, "PNG", quality=95)
    
    print(f"✅ Sample prescription created: {png_path}")
    print(f"📏 Size: {prescription.width}x{prescription.height} pixels")
    print("\n🔖 Ready for document stamping!")
    print("You can now use this file to test the document stamping system:")
    print(f"  - Web interface: http://localhost:8000/static/document_stamper.html")
    print(f"  - CLI: .\\venv\\Scripts\\python.exe document_stamper_cli.py {png_path}")
    
    return png_path

if __name__ == "__main__":
    main()