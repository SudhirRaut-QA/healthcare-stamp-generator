#!/usr/bin/env python3
"""
Interactive Hospital Stamp Generator - Just enter your hospital name!
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.modules.stamp_generator.generator import HospitalStampGenerator, StampStyle

def interactive_stamp_generator():
    """Interactive way to generate stamps for your specific hospital names"""
    generator = HospitalStampGenerator()
    
    print("🏥 Interactive Hospital Stamp Generator")
    print("=" * 45)
    print("✨ Enter your hospital names and get instant stamps!")
    
    while True:
        print("\n" + "="*50)
        print("📝 Enter Hospital Name (or 'quit' to exit):")
        hospital_name = input("🏥 Hospital Name: ").strip()
        
        if hospital_name.lower() in ['quit', 'exit', 'q']:
            print("👋 Thank you for using the Hospital Stamp Generator!")
            break
        
        if not hospital_name:
            print("❌ Please enter a hospital name!")
            continue
        
        # Analyze the name
        word_count = len(hospital_name.split())
        char_count = len(hospital_name)
        
        print(f"\n📊 Analysis:")
        print(f"   • Hospital: {hospital_name}")
        print(f"   • Words: {word_count}")
        print(f"   • Characters: {char_count}")
        
        if word_count > 5:
            print(f"   ⚠️  Many words detected - applying overlap protection")
        
        # Generate the stamp
        try:
            print(f"\n⏳ Generating stamp...")
            
            stamp_data = generator.generate_stamp(
                hospital_name=hospital_name,
                size=420,  # Good size for readability
                style=StampStyle.OFFICIAL,
                border_style="double"
            )
            
            # Save to file
            clean_name = hospital_name.replace(' ', '_').replace('.', '').replace("'", '').replace('/', '_').lower()
            timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"custom_{timestamp}_{clean_name}.png"
            filepath = os.path.join(generator.output_folder, filename)
            
            with open(filepath, 'wb') as f:
                f.write(stamp_data)
            
            print(f"✅ SUCCESS! Stamp generated:")
            print(f"   📁 File: {filename}")
            print(f"   📝 Display: ● {hospital_name.upper()}")
            print(f"   📏 Size: 420x420 pixels")
            print(f"   🎯 Style: Official with double border")
            
            if word_count > 5:
                print(f"   🔧 Overlap protection applied for {word_count} words")
            
        except Exception as e:
            print(f"❌ Error generating stamp: {str(e)}")
            print(f"💡 Try a shorter name or check for special characters")
    
    print(f"\n📁 All your stamps are saved in: {generator.output_folder}/")

def quick_examples():
    """Show some quick examples"""
    generator = HospitalStampGenerator()
    
    print("\n🎯 Quick Examples:")
    print("-" * 25)
    
    examples = [
        "Central Hospital",
        "Mayo Clinic Medical Center", 
        "Johns Hopkins University Hospital"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. Example: {example}")
        
        stamp_data = generator.generate_stamp(
            hospital_name=example,
            size=400,
            style=StampStyle.OFFICIAL
        )
        
        clean_name = example.replace(' ', '_').lower()
        filename = f"example_{i}_{clean_name}.png"
        filepath = os.path.join(generator.output_folder, filename)
        
        with open(filepath, 'wb') as f:
            f.write(stamp_data)
        
        print(f"   ✅ Generated: {filename}")
    
    print(f"\n📁 Examples saved to: {generator.output_folder}/")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Interactive Generator (enter names one by one)")
    print("2. Quick Examples")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        interactive_stamp_generator()
    elif choice == "2":
        quick_examples()
    else:
        print("Running interactive generator by default...")
        interactive_stamp_generator()