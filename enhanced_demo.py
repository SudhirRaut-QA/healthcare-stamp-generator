"""
Enhanced Hospital Stamp Generator Demo
Showcases all the new features and enhancements
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.modules.stamp_generator import HospitalStampGenerator, StampStyle, StampColor

def demonstrate_basic_features():
    """Demonstrate basic stamp generation with output folder"""
    print("🏥 Basic Stamp Generation")
    print("=" * 50)
    
    generator = HospitalStampGenerator()
    hospitals = [
        "City General Hospital",
        "St. Mary's Medical Center", 
        "Children's Hospital"
    ]
    
    for hospital in hospitals:
        output_path = generator.save_stamp_to_output(hospital)
        print(f"✅ Created: {output_path}")
    print()

def demonstrate_style_variations():
    """Demonstrate different stamp styles"""
    print("🎨 Style Variations")
    print("=" * 50)
    
    generator = HospitalStampGenerator()
    hospital_name = "Metropolitan Hospital"
    
    styles = [
        (StampStyle.CLASSIC, StampColor.BLUE, "double"),
        (StampStyle.MODERN, StampColor.GREEN, "single"),
        (StampStyle.OFFICIAL, StampColor.NAVY, "triple"),
        (StampStyle.EMERGENCY, StampColor.RED, "double")
    ]
    
    for style, color, border in styles:
        filename = f"{hospital_name.replace(' ', '_')}_{style.value}.png"
        output_path = generator.save_stamp_to_output(
            hospital_name,
            filename=filename,
            style=style,
            color=color.value,
            border_style=border,
            size=350
        )
        print(f"✅ {style.value.title()} style: {output_path}")
    print()

def demonstrate_enhanced_features():
    """Demonstrate enhanced features like date and logos"""
    print("⭐ Enhanced Features")
    print("=" * 50)
    
    generator = HospitalStampGenerator()
    
    # Enhanced stamp with all features
    enhanced_path = generator.save_stamp_to_output(
        "Advanced Medical Center",
        filename="advanced_with_date.png",
        style=StampStyle.OFFICIAL,
        color=StampColor.NAVY.value,
        border_style="triple",
        include_date=True,
        include_logo=True,
        size=400
    )
    print(f"✅ Enhanced stamp with date: {enhanced_path}")
    
    # Custom color stamp
    custom_color = (128, 0, 128, 255)  # Purple
    custom_path = generator.save_stamp_to_output(
        "Specialty Clinic",
        filename="custom_purple.png",
        color=custom_color,
        size=320
    )
    print(f"✅ Custom purple stamp: {custom_path}")
    print()

def demonstrate_batch_variants():
    """Demonstrate creating multiple variants at once"""
    print("📦 Batch Variant Creation")
    print("=" * 50)
    
    generator = HospitalStampGenerator()
    
    hospitals = [
        "Regional Medical Center",
        "University Hospital",
        "Community Health Clinic"
    ]
    
    for hospital in hospitals:
        print(f"Creating variants for: {hospital}")
        variants = generator.create_stamp_variants(hospital)
        for variant_type, path in variants.items():
            print(f"  - {variant_type.title()}: {os.path.basename(path)}")
    print()

def demonstrate_size_options():
    """Demonstrate different size options"""
    print("📏 Size Options")
    print("=" * 50)
    
    generator = HospitalStampGenerator()
    hospital_name = "Multi-Size Hospital"
    
    sizes = [250, 300, 350, 400, 450]
    for size in sizes:
        filename = f"size_{size}px.png"
        output_path = generator.save_stamp_to_output(
            hospital_name,
            filename=filename,
            size=size
        )
        print(f"✅ {size}px stamp: {output_path}")
    print()

def show_output_folder_contents():
    """Show what's in the output folder"""
    print("📁 Output Folder Contents")
    print("=" * 50)
    
    output_folder = "stampOutput"
    if os.path.exists(output_folder):
        files = os.listdir(output_folder)
        if files:
            print(f"Found {len(files)} stamp files:")
            for file in sorted(files):
                file_path = os.path.join(output_folder, file)
                file_size = os.path.getsize(file_path)
                print(f"  📄 {file} ({file_size:,} bytes)")
        else:
            print("No stamp files found.")
    else:
        print("Output folder doesn't exist yet.")
    print()

def main():
    """Main demonstration function"""
    print("🌟 Enhanced Hospital Stamp Generator Demo")
    print("=" * 60)
    print("This demo showcases all the new features and enhancements!")
    print()
    
    # Run all demonstrations
    demonstrate_basic_features()
    demonstrate_style_variations()
    demonstrate_enhanced_features()
    demonstrate_batch_variants()
    demonstrate_size_options()
    show_output_folder_contents()
    
    print("🎉 Demo Complete!")
    print("=" * 60)
    print("✨ New Features Demonstrated:")
    print("  • Automatic output folder organization")
    print("  • Multiple stamp styles (Classic, Modern, Official, Emergency)")
    print("  • Customizable colors and borders")
    print("  • Date inclusion option")
    print("  • Enhanced medical symbols")
    print("  • Batch variant creation")
    print("  • Multiple size options")
    print("  • Timestamped filenames")
    print()
    print(f"📁 All stamps saved to: {os.path.abspath('stampOutput')}")

if __name__ == "__main__":
    main()