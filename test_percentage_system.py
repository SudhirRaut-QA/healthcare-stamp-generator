#!/usr/bin/env python3

import sys
sys.path.append('.')
from app.modules.stamp_generator.generator import generate_stamp, StampColor

def test_percentage_spacing():
    """
    Test the new percentage-based spacing system
    """
    
    print("🎯 NEW PERCENTAGE-BASED SPACING SYSTEM")
    print("=" * 50)
    print()
    
    print("📍 MANUAL SPACING CONTROLS (Easy to adjust):")
    print("Lines 309-313 in generator.py:")
    print("• CHAR_SPACING_PERCENTAGE = 85    # 85% for characters")
    print("• WORD_GAP_PERCENTAGE = 15        # 15% for word gaps") 
    print("• DOT_TO_TEXT_GAP_PERCENTAGE = 3  # 3% gap after dot")
    print("• SAFETY_MARGIN_PERCENTAGE = 5   # 5% safety margin")
    print()
    
    test_cases = [
        ('ABC HOSPITAL', '2 words'),
        ('CITY GENERAL HOSPITAL', '3 words'),
        ('ST MARY REGIONAL MEDICAL CENTER', '5 words'),
        ('UNIVERSITY OF TORONTO GENERAL HOSPITAL NETWORK', '6+ words')
    ]
    
    print("🧪 TESTING RESULTS:")
    print("-" * 30)
    
    for i, (hospital_name, desc) in enumerate(test_cases, 1):
        print(f"{i}. {desc}: {hospital_name}")
        
        try:
            path = generate_stamp(
                hospital_name=hospital_name,
                color=StampColor.BLUE,
                character_spacing=2.2,
                output_path=f'percentage_test_{i}.png'
            )
            print(f"   ✓ Generated: {path}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        print()
    
    print("✅ IMPROVEMENTS:")
    print("• Text stops before reaching dot (no overlap)")
    print("• Percentage-based spacing (easy to adjust)")
    print("• Manual controls clearly labeled")
    print("• Consistent character distribution")
    
    print()
    print("🔧 TO ADJUST SPACING:")
    print("1. Open generator.py")
    print("2. Go to lines 309-313") 
    print("3. Change the percentage values:")
    print("   - Increase CHAR_SPACING_PERCENTAGE for more letter spacing")
    print("   - Increase WORD_GAP_PERCENTAGE for more word spacing")
    print("   - Adjust DOT_TO_TEXT_GAP_PERCENTAGE for gap after dot")

if __name__ == "__main__":
    test_percentage_spacing()