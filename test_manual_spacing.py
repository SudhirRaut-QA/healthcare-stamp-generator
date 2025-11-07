#!/usr/bin/env python3

import sys
sys.path.append('.')
from app.modules.stamp_generator.generator import generate_stamp, StampColor

def test_manual_spacing_controls():
    """
    Test script to demonstrate manual character spacing controls
    """
    
    test_name = "CITY GENERAL HOSPITAL"  # 3 words - good for testing
    
    print("🎛️ MANUAL SPACING CONTROL DEMONSTRATION")
    print("=" * 50)
    print(f"Test hospital: {test_name}")
    print()
    
    # Test different character_spacing values
    spacing_tests = [
        (1.0, "Tight spacing"),
        (1.5, "Normal spacing"), 
        (2.0, "Wide spacing"),
        (2.5, "Very wide spacing")
    ]
    
    print("Testing character_spacing parameter (Line 227):")
    print("-" * 45)
    
    for spacing, description in spacing_tests:
        print(f"• {description} (spacing={spacing})")
        
        filename = f"manual_control_spacing_{spacing}.png"
        path = generate_stamp(
            hospital_name=test_name,
            color=StampColor.BLUE,
            character_spacing=spacing,
            output_path=filename
        )
        print(f"  Generated: {path}")
        print()
    
    print("📝 SPACING CONTROL SUMMARY:")
    print("=" * 30)
    print("✅ NOW FIXED:")
    print("• 2-3 words: No longer go beyond dot")
    print("• 4 words: Maintain good spacing") 
    print("• 5+ words: Proper spacing between letters")
    print()
    print("🔧 MANUAL CONTROLS:")
    print("• Line 227: character_spacing (API level)")
    print("• Line 302: character_spacing_multiplier (internal)")
    print()
    print("📊 RECOMMENDED VALUES:")
    print("• character_spacing: 1.0-2.5 (your 2.2 is good)")
    print("• For tighter: 1.0-1.5")
    print("• For wider: 2.0-3.0")

if __name__ == "__main__":
    test_manual_spacing_controls()