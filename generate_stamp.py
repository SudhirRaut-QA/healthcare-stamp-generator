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
    
    # Generate output filename if not provided
    if args.output is None:
        safe_name = "".join(c for c in args.hospital_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        args.output = f"{safe_name}_stamp.png"
    
    try:
        # Generate and save stamp
        print(f"Generating stamp for: {args.hospital_name}")
        print(f"Size: {args.size}x{args.size} pixels")
        print(f"Output file: {args.output}")
        
        generator.save_stamp(
            hospital_name=args.hospital_name,
            filename=args.output,
            size=args.size
        )
        
        print(f"✅ Stamp generated successfully: {args.output}")
        print("Features:")
        print("  - Circular design with blue ink")
        print("  - Transparent background")
        print("  - Professional medical appearance")
        print("  - Ready for prescription printing")
        
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
        print("Generating example stamp...")
        
        generator = HospitalStampGenerator()
        generator.save_stamp("EXAMPLE MEDICAL CENTER", "example_stamp.png")
        print("✅ Example stamp saved as: example_stamp.png")
    else:
        main()