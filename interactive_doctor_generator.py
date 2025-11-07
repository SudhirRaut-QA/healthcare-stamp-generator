#!/usr/bin/env python3
"""
🩺 Interactive Doctor Stamp Generator

User-friendly interactive interface for generating professional doctor stamps.
Perfect for healthcare administrators and medical professionals.
"""

import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.modules.doctor_stamp.generator import DoctorStampGenerator


def get_user_input(prompt: str, required: bool = True) -> str:
    """Get user input with validation."""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("❌ This field is required. Please try again.")


def get_numeric_input(prompt: str, min_val: int, max_val: int, default: int) -> int:
    """Get numeric input with validation."""
    while True:
        value = input(f"{prompt} (default: {default}): ").strip()
        if not value:
            return default
        try:
            num = int(value)
            if min_val <= num <= max_val:
                return num
            else:
                print(f"❌ Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print("❌ Please enter a valid number")


def display_banner():
    """Display application banner."""
    print("=" * 60)
    print("🩺 INTERACTIVE DOCTOR STAMP GENERATOR")
    print("   Professional Medical Stamps Made Easy")
    print("=" * 60)
    print()


def display_examples():
    """Display example inputs for user guidance."""
    print("📝 Example inputs:")
    print("   Doctor Name: Dr. Sarah Johnson")
    print("   Degree: MBBS, MD (Cardiology)")
    print("   Registration: Reg. No: MCI-12345")
    print()


def display_features():
    """Display stamp features."""
    print("✨ Your doctor stamp will include:")
    print("   • Clean rectangular layout")
    print("   • Doctor's name (largest, bold font with shadow)")
    print("   • Medical degree/qualification (medium font)")
    print("   • Registration number (smallest font)")
    print("   • Borderless design for clean appearance")
    print("   • Realistic ink blue text (#2F4F8F) for authentic appearance")
    print("   • Realistic medical fonts (Times New Roman priority)")
    print("   • Transparent PNG background")
    print("   • Scalable sizing with proportional fonts")
    print()


def generate_single_stamp():
    """Generate a single doctor stamp interactively."""
    print("📋 DOCTOR STAMP DETAILS")
    print("-" * 30)
    
    # Get doctor information
    doctor_name = get_user_input("👨‍⚕️ Doctor's full name (e.g., Dr. Sarah Johnson): ")
    degree = get_user_input("🎓 Medical degree/qualification (e.g., MBBS, MD (Cardiology)): ")
    registration = get_user_input("📋 Registration number (e.g., Reg. No: MCI-12345): ")
    
    print("\n📏 STAMP DIMENSIONS")
    print("-" * 20)
    width = get_numeric_input("🔲 Width in pixels", 200, 800, 400)
    height = get_numeric_input("📐 Height in pixels", 100, 400, 200)
    
    # Generate stamp
    generator = DoctorStampGenerator()
    
    print(f"\n🔄 Generating stamp for: {doctor_name}")
    print(f"📏 Size: {width}x{height} pixels")
    
    try:
        output_path = generator.generate_doctor_stamp(
            doctor_name=doctor_name,
            degree=degree,
            registration_number=registration,
            width=width,
            height=height
        )
        
        print(f"✅ Doctor stamp generated successfully!")
        print(f"📁 File saved to: {output_path}")
        print("🌟 Professional medical stamp ready!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating stamp: {e}")
        return False


def generate_batch_stamps():
    """Generate multiple doctor stamps."""
    print("📋 BATCH DOCTOR STAMP GENERATION")
    print("-" * 35)
    
    doctors_data = []
    
    while True:
        print(f"\n👨‍⚕️ Doctor #{len(doctors_data) + 1}")
        print("-" * 15)
        
        doctor_name = get_user_input("Doctor's full name: ")
        degree = get_user_input("Medical degree: ")
        registration = get_user_input("Registration number: ")
        
        doctors_data.append({
            'name': doctor_name,
            'degree': degree,
            'registration': registration
        })
        
        another = input("\n➕ Add another doctor? (y/n): ").strip().lower()
        if another not in ['y', 'yes']:
            break
    
    # Generate all stamps
    generator = DoctorStampGenerator()
    
    print(f"\n🔄 Generating {len(doctors_data)} doctor stamps...")
    
    try:
        generated_files = generator.generate_batch_stamps(doctors_data)
        
        print(f"✅ Successfully generated {len(generated_files)} doctor stamps!")
        print("📁 Files saved:")
        for file_path in generated_files:
            print(f"   • {file_path}")
        print("🌟 All professional medical stamps ready!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating batch stamps: {e}")
        return False


def main():
    """Main interactive loop."""
    display_banner()
    
    while True:
        print("🎛️ MAIN MENU")
        print("-" * 12)
        print("1. Generate single doctor stamp")
        print("2. Generate multiple doctor stamps (batch)")
        print("3. View stamp features")
        print("4. View examples")
        print("5. Exit")
        print()
        
        choice = input("👉 Select an option (1-5): ").strip()
        
        if choice == "1":
            print("\n" + "="*60)
            generate_single_stamp()
            
        elif choice == "2":
            print("\n" + "="*60)
            generate_batch_stamps()
            
        elif choice == "3":
            print("\n" + "="*60)
            display_features()
            
        elif choice == "4":
            print("\n" + "="*60)
            display_examples()
            
        elif choice == "5":
            print("\n👋 Thank you for using Doctor Stamp Generator!")
            print("🩺 Your professional medical stamps are ready!")
            break
            
        else:
            print("❌ Invalid option. Please select 1-5.")
        
        if choice in ["1", "2", "3", "4"]:
            input("\n📋 Press Enter to continue...")
            print("\n" + "="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Doctor Stamp Generator closed. Have a great day!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please contact support if this issue persists.")