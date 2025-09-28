"""
Hospital Stamp Generator - Quick Reference Guide
Different ways to create stamps with various hospital names
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.modules.stamp_generator import HospitalStampGenerator
import requests
import json

def method_1_standalone_script():
    """Method 1: Using the standalone script"""
    print("🔧 Method 1: Using Standalone Script")
    print("=" * 50)
    print("Command examples:")
    print('python generate_stamp.py "Your Hospital Name"')
    print('python generate_stamp.py "Medical Center" --size 400')
    print('python generate_stamp.py "Clinic Name" --output custom_name.png')
    print()

def method_2_direct_python():
    """Method 2: Using Python code directly"""
    print("🐍 Method 2: Direct Python Code")
    print("=" * 50)
    
    # Create generator instance
    generator = HospitalStampGenerator()
    
    # List of hospital names to create stamps for
    hospitals = [
        "Emergency Medical Center",
        "Pediatric Hospital",
        "Cardiac Care Institute",
        "Women's Health Clinic"
    ]
    
    for hospital in hospitals:
        try:
            filename = f"{hospital.replace(' ', '_').replace("'", "")}_stamp.png"
            generator.save_stamp(hospital, filename, size=320)
            print(f"✅ Created: {filename}")
        except Exception as e:
            print(f"❌ Error creating stamp for {hospital}: {e}")
    print()

def method_3_api_calls():
    """Method 3: Using the API (if server is running)"""
    print("🌐 Method 3: Using API Calls")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("✅ Server is running!")
            
            # Example API calls
            hospitals = ["Regional Medical Center", "Community Hospital"]
            
            for hospital in hospitals:
                try:
                    # Make API call
                    api_response = requests.post(
                        "http://localhost:8000/api/v1/stamp/generate",
                        json={"hospital_name": hospital, "size": 300},
                        timeout=10
                    )
                    
                    if api_response.status_code == 200:
                        # Save the stamp
                        filename = f"api_{hospital.replace(' ', '_')}_stamp.png"
                        with open(filename, "wb") as f:
                            f.write(api_response.content)
                        print(f"✅ API created: {filename}")
                    else:
                        print(f"❌ API error for {hospital}: {api_response.status_code}")
                        
                except requests.exceptions.RequestException as e:
                    print(f"❌ API call failed for {hospital}: {e}")
        else:
            print("⚠️ Server responded but not healthy")
            
    except requests.exceptions.RequestException:
        print("⚠️ Server is not running. Start it with:")
        print("uvicorn app.main:app --reload")
    print()

def method_4_batch_creation():
    """Method 4: Batch creation of multiple stamps"""
    print("📦 Method 4: Batch Creation")
    print("=" * 50)
    
    generator = HospitalStampGenerator()
    
    # Hospital configurations
    hospital_configs = [
        {"name": "City General Hospital", "size": 300},
        {"name": "St. Mary's Medical Center", "size": 350},
        {"name": "University Hospital", "size": 280},
        {"name": "Children's Hospital", "size": 400},
        {"name": "Veterans Medical Center", "size": 320}
    ]
    
    print("Creating multiple stamps...")
    for config in hospital_configs:
        try:
            safe_name = config["name"].replace(" ", "_").replace("'", "")
            filename = f"batch_{safe_name}_{config['size']}px.png"
            
            generator.save_stamp(
                hospital_name=config["name"],
                filename=filename,
                size=config["size"]
            )
            print(f"✅ {config['name']} → {filename}")
            
        except Exception as e:
            print(f"❌ Error with {config['name']}: {e}")
    print()

def show_customization_options():
    """Show all customization options"""
    print("🎨 Customization Options")
    print("=" * 50)
    print("Available parameters:")
    print("• hospital_name: The name to display on the stamp")
    print("• size: Stamp diameter in pixels (100-800)")
    print("• font_size: Text size (auto-calculated if not specified)")
    print("• color: RGBA color tuple (default: blue)")
    print()
    print("Example with custom color:")
    
    generator = HospitalStampGenerator()
    # Create a stamp with custom red color
    red_color = (200, 50, 50, 255)  # Red RGBA
    stamp_bytes = generator.generate_stamp(
        hospital_name="Custom Color Hospital",
        size=300,
        color=red_color
    )
    
    with open("custom_red_stamp.png", "wb") as f:
        f.write(stamp_bytes)
    print("✅ Created custom red stamp: custom_red_stamp.png")
    print()

def main():
    """Main demonstration function"""
    print("🏥 Hospital Stamp Generator - All Methods")
    print("=" * 60)
    print()
    
    # Show all methods
    method_1_standalone_script()
    method_2_direct_python()
    method_3_api_calls()
    method_4_batch_creation()
    show_customization_options()
    
    print("🎉 Summary:")
    print("All demonstration stamps have been created!")
    print("Check the current directory for the generated PNG files.")
    print()
    print("💡 Pro Tips:")
    print("• Use Method 1 for quick single stamps")
    print("• Use Method 2 for Python integration")
    print("• Use Method 3 for web applications")
    print("• Use Method 4 for bulk creation")

if __name__ == "__main__":
    main()