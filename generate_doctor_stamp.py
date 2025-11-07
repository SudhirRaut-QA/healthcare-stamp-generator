#!/usr/bin/env python3
"""
🩺 Doctor Stamp Generator - Command Line Interface

Generate professional rectangular doctor stamps with authentic medical appearance.

Usage:
    python generate_doctor_stamp.py "Dr. Sarah Johnson" "MBBS, MD (Cardiology)" "Reg. No: MCI-12345"
    python generate_doctor_stamp.py "Dr. Michael Chen" "MBBS, MS (Orthopedics)" "Reg. No: MCI-67890" --width 500 --height 250

Features:
- Professional rectangular layout
- Three-tier text hierarchy (Name > Degree > Registration)
- Authentic medical appearance with professional borders
- Transparent PNG background
- Scalable sizing with proportional fonts
"""

import argparse
import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.modules.doctor_stamp.generator import DoctorStampGenerator


def main():
    parser = argparse.ArgumentParser(
        description="🩺 Generate professional doctor stamps",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Dr. Sarah Johnson" "MBBS, MD (Cardiology)" "MCI-12345"
  %(prog)s "Dr. Michael Chen" "MBBS, MS (Orthopedics)" "MCI-67890" --width 500 --height 250
  %(prog)s "Dr. Priya Sharma" "MBBS, DGO, MD (Gynecology)" "Reg. No: MCI-11223" --output "custom_stamp.png"

Note: You can provide just the registration number (e.g., 'MCI-12345') or include the full text (e.g., 'Reg. No: MCI-12345').
The 'Reg. No.:' prefix will be automatically added if not present.

The generated stamp will have:
  • Doctor's name (largest, bold font)
  • Medical degree/qualification (medium font)  
  • Registration number (smallest font)
  • Professional rectangular layout with borders
  • Transparent background for easy integration
        """
    )
    
    parser.add_argument("doctor_name", help="Doctor's full name (e.g., 'Dr. Sarah Johnson')")
    parser.add_argument("degree", help="Medical degree/qualification (e.g., 'MBBS, MD (Cardiology)')")
    parser.add_argument("registration", help="Medical registration number (e.g., 'MCI-12345' or 'Reg. No: MCI-12345' - prefix auto-added if missing)")
    
    parser.add_argument("--width", type=int, default=400, 
                       help="Stamp width in pixels (default: 400)")
    parser.add_argument("--height", type=int, default=200,
                       help="Stamp height in pixels (default: 200)")
    parser.add_argument("--output", type=str,
                       help="Custom output file path (default: auto-generated)")
    
    args = parser.parse_args()
    
    # Validate dimensions
    if args.width < 200 or args.width > 800:
        print("❌ Error: Width must be between 200 and 800 pixels")
        sys.exit(1)
        
    if args.height < 100 or args.height > 400:
        print("❌ Error: Height must be between 100 and 400 pixels")
        sys.exit(1)
    
    # Create doctor stamp generator
    generator = DoctorStampGenerator()
    
    print(f"🩺 Generating doctor stamp for: {args.doctor_name}")
    print(f"📏 Size: {args.width}x{args.height} pixels")
    print(f"🎓 Degree: {args.degree}")
    print(f"📋 Registration: {args.registration}")
    
    try:
        # Generate the stamp
        output_path = generator.generate_doctor_stamp(
            doctor_name=args.doctor_name,
            degree=args.degree,
            registration_number=args.registration,
            width=args.width,
            height=args.height,
            output_path=args.output
        )
        
        print(f"✅ Doctor stamp generated successfully: {output_path}")
        print("🌟 Professional medical stamp ready!")
        print("Features:")
        print("  - Clean rectangular layout")
        print("  - Three-tier text hierarchy")
        print("  - Realistic ink blue text (#2F4F8F) for authentic appearance")
        print("  - Enhanced visibility with realistic fonts")
        print("  - Borderless design")
        print("  - Transparent background")
        print("  - Saved to doctorStampOutput folder")
        
    except Exception as e:
        print(f"❌ Error generating doctor stamp: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()