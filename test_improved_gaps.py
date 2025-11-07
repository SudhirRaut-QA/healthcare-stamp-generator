#!/usr/bin/env python3

import sys
sys.path.append('.')
from app.modules.stamp_generator.generator import generate_stamp, StampColor

# Test with different text lengths to verify improved percentage-based gaps
test_cases = [
    'ABC HOSPITAL',  # 2 words
    'CITY GENERAL HOSPITAL',  # 3 words  
    'ST MARY REGIONAL MEDICAL CENTER',  # 5 words
    'UNIVERSITY OF TORONTO GENERAL HOSPITAL NETWORK'  # 6 words
]

print("Testing improved percentage-based gap system...")
print("=" * 60)

for i, hospital_name in enumerate(test_cases, 1):
    print(f'Test {i}: {hospital_name}')
    print(f'  Words: {len(hospital_name.split())}, Characters: {len(hospital_name)}')
    
    try:
        stamp_path = generate_stamp(
            hospital_name=hospital_name,
            hospital_address='123 Main St',
            stamp_date='2024-01-15',
            color=StampColor.BLUE,
            character_spacing=1.2,
            output_path=f'test_improved_gaps_{i}.png'
        )
        print(f'  ✓ Generated: {stamp_path}')
    except Exception as e:
        print(f'  ✗ Error: {e}')
    print()

print("All test stamps generated with improved percentage-based gaps!")
print("Check the generated PNG files to verify:")
print("1. Full circle coverage for all text lengths")
print("2. Proper spacing between characters (no overlap)")
print("3. Consistent gap between dot and first letter")
print("4. Justified text appearance across the full circle")