"""
Standalone script to test and demonstrate the hospital stamp generator
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.modules.stamp_generator import HospitalStampGenerator
import argparse


def main():
    """Main function to test stamp generation"""
    parser = argparse.ArgumentParser(description='Generate hospital stamps')
    parser.add_argument('hospital_name', help='Name of the hospital')
    parser.add_argument('--size', type=int, default=300, help='Size of the stamp (default: 300)')
    parser.add_argument('--output', '-o', default=None, help='Output filename (default: auto-generated)')
    
    args = parser.parse_args()
    
    # Create generator
    generator = HospitalStampGenerator()
    
    try:
        print(f"🏥 Generating stamp for: {args.hospital_name}")
        print(f"📏 Size: {args.size}x{args.size} pixels")
        
        # Get dynamic parameters for analysis
        params = generator._calculate_dynamic_parameters(args.hospital_name, args.size)
        print(f"🔧 Dynamic Analysis:")
        print(f"   • Font size: {params['font_size']}px (auto-optimized)")
        print(f"   • Text radius: {params['text_radius']}px")
        print(f"   • Character spacing: {params['char_spacing']:.1f}° (no overlap)")
        print(f"   • Gap width: {params['gap_width']}px")
        
        # Generate stamp with dynamic precision
        if args.output is None:
            # Auto-generate filename
            clean_name = args.hospital_name.replace(' ', '_').replace('.', '').replace("'", '').lower()
            filename = f"stamp_{clean_name}.png"
            output_path = os.path.join("stampOutput", filename)
        else:
            # Use custom filename
            output_path = os.path.join("stampOutput", args.output)
            
        generator.save_stamp(
            hospital_name=args.hospital_name,
            filename=output_path,
            size=args.size
        )
        
        print(f"✅ Stamp generated successfully: {output_path}")
        print(f"🌟 Dynamic precision applied - perfect fit guaranteed!")
        
        print("Features:")
        print("  - Circular design with customizable colors")
        print("  - Transparent background")
        print("  - Professional medical appearance")
        print("  - Multiple style options")
        print("  - Saved to stampOutput folder")
        
    except Exception as e:
        print(f"❌ Error generating stamp: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Example usage if no arguments provided
    if len(sys.argv) == 1:
        print("Hospital Stamp Generator")
        print("=" * 50)
        print()
        print("Usage:")
        print("  python generate_stamp.py 'City General Hospital'")
        print("  python generate_stamp.py 'Medical Center' --size 400")
        print("  python generate_stamp.py 'Hospital Name' --output my_stamp.png")
        print()
        print("Generating example stamps...")
        
        generator = HospitalStampGenerator()
        # Create multiple example stamps with different styles
        variants = generator.create_stamp_variants("EXAMPLE MEDICAL CENTER")
        
        print("✅ Example stamps created:")
        for style, path in variants.items():
            print(f"   - {style.title()}: {path}")
    else:
        main()