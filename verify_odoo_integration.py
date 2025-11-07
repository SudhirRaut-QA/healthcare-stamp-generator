"""
Odoo Integration Verification Script
Checks if all components are ready for Odoo integration
"""

import os
import sys
from pathlib import Path

def print_status(message, status):
    """Print colored status message"""
    symbols = {"✅": "PASS", "❌": "FAIL", "⚠️": "WARN", "ℹ️": "INFO"}
    print(f"{symbols.get(status, status)} {message}")

def check_prerequisites():
    """Check Python and dependencies"""
    print("\n" + "="*60)
    print("📋 PREREQUISITE CHECK")
    print("="*60)
    
    # Python version
    python_version = sys.version_info
    if python_version >= (3, 8):
        print_status(f"Python {python_version.major}.{python_version.minor} installed", "✅")
    else:
        print_status(f"Python {python_version.major}.{python_version.minor} (need 3.8+)", "❌")
    
    # PIL/Pillow
    try:
        from PIL import Image
        import PIL
        print_status(f"Pillow {PIL.__version__} installed", "✅")
    except ImportError:
        print_status("Pillow NOT installed - Run: pip install Pillow", "❌")
    
    # FastAPI (optional)
    try:
        import fastapi
        print_status(f"FastAPI {fastapi.__version__} installed", "✅")
    except ImportError:
        print_status("FastAPI not installed (optional)", "⚠️")

def check_module_structure():
    """Check Odoo module structure"""
    print("\n" + "="*60)
    print("📁 MODULE STRUCTURE CHECK")
    print("="*60)
    
    base_path = Path(__file__).parent / "odoo_integration"
    
    required_files = [
        "__manifest__.py",
        "__init__.py",
        "models/__init__.py",
        "models/hospital_stamp.py",
        "models/doctor_stamp.py",
        "lib/__init__.py",
        "lib/hospital_generator.py",
        "lib/doctor_generator.py",
        "views/menu_views.xml",
        "views/hospital_stamp_views.xml",
        "views/doctor_stamp_views.xml",
        "security/ir.model.access.csv",
    ]
    
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print_status(f"{file_path}", "✅")
        else:
            print_status(f"{file_path} - MISSING", "❌")

def check_core_generator():
    """Check core stamp generator"""
    print("\n" + "="*60)
    print("🏥 CORE GENERATOR CHECK")
    print("="*60)
    
    base_path = Path(__file__).parent / "app"
    
    required_files = [
        "modules/stamp_generator/generator.py",
        "modules/stamp_generator/__init__.py",
        "modules/doctor_stamp_generator/generator.py",
        "modules/doctor_stamp_generator/__init__.py",
    ]
    
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print_status(f"{file_path}", "✅")
        else:
            print_status(f"{file_path} - MISSING", "❌")
    
    # Test imports
    try:
        sys.path.insert(0, str(base_path))
        from modules.stamp_generator.generator import HospitalStampGenerator
        print_status("HospitalStampGenerator import successful", "✅")
    except ImportError as e:
        print_status(f"HospitalStampGenerator import failed: {e}", "❌")
    
    try:
        from modules.doctor_stamp_generator.generator import DoctorStampGenerator
        print_status("DoctorStampGenerator import successful", "✅")
    except ImportError as e:
        print_status(f"DoctorStampGenerator import failed: {e}", "❌")

def check_adapter_paths():
    """Check adapter file paths"""
    print("\n" + "="*60)
    print("🔗 ADAPTER PATH CHECK")
    print("="*60)
    
    adapter_file = Path(__file__).parent / "odoo_integration/lib/hospital_generator.py"
    
    if adapter_file.exists():
        with open(adapter_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if using absolute or relative path
        if "app_path = os.path.join" in content:
            print_status("Using relative path (might need adjustment)", "⚠️")
            print("   → Consider using absolute path for production")
        elif "app_path = r\"" in content:
            print_status("Using absolute path", "✅")
        else:
            print_status("Path configuration unclear", "⚠️")
    else:
        print_status("hospital_generator.py not found", "❌")

def test_stamp_generation():
    """Test stamp generation"""
    print("\n" + "="*60)
    print("🧪 STAMP GENERATION TEST")
    print("="*60)
    
    try:
        base_path = Path(__file__).parent / "app"
        sys.path.insert(0, str(base_path))
        
        from modules.stamp_generator.generator import HospitalStampGenerator
        
        generator = HospitalStampGenerator()
        stamp_bytes = generator.generate_stamp_bytes("Test Hospital", size=300)
        
        if stamp_bytes and len(stamp_bytes) > 0:
            print_status(f"Hospital stamp generated ({len(stamp_bytes)} bytes)", "✅")
        else:
            print_status("Hospital stamp generation failed", "❌")
            
    except Exception as e:
        print_status(f"Stamp generation test failed: {e}", "❌")
    
    try:
        from modules.doctor_stamp_generator.generator import DoctorStampGenerator
        
        generator = DoctorStampGenerator()
        stamp_bytes = generator.generate_stamp(
            name="Dr. Test",
            degree="MBBS",
            registration_number="REG-12345",
            output_path=None
        )
        
        if stamp_bytes and len(stamp_bytes) > 0:
            print_status(f"Doctor stamp generated ({len(stamp_bytes)} bytes)", "✅")
        else:
            print_status("Doctor stamp generation failed", "❌")
            
    except Exception as e:
        print_status(f"Doctor stamp test failed: {e}", "❌")

def generate_integration_summary():
    """Generate integration summary"""
    print("\n" + "="*60)
    print("📊 INTEGRATION SUMMARY")
    print("="*60)
    
    print("\n🎯 NEXT STEPS:")
    print("\n1. Copy module to Odoo:")
    print("   Copy-Item 'odoo_integration' -Destination 'C:\\path\\to\\odoo\\addons\\healthcare_stamp' -Recurse")
    
    print("\n2. Update adapter paths:")
    print("   Edit: odoo_integration/lib/hospital_generator.py")
    print("   Update app_path to absolute path")
    
    print("\n3. Restart Odoo:")
    print("   Restart-Service Odoo")
    
    print("\n4. Install module:")
    print("   Odoo → Apps → Update Apps List → Search 'Healthcare Stamp' → Install")
    
    print("\n5. Test generation:")
    print("   Healthcare → Hospital Stamps → Create → Generate Stamp")
    
    print("\n📚 Documentation:")
    print("   - ODOO_INTEGRATION_STEPS.md (detailed guide)")
    print("   - odoo_integration/INTEGRATION_GUIDE.md")
    print("   - odoo_integration/README.md")

def main():
    """Run all checks"""
    print("\n" + "🏥 HEALTHCARE STAMP GENERATOR - ODOO INTEGRATION VERIFICATION" + "\n")
    
    check_prerequisites()
    check_module_structure()
    check_core_generator()
    check_adapter_paths()
    test_stamp_generation()
    generate_integration_summary()
    
    print("\n" + "="*60)
    print("✅ VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
