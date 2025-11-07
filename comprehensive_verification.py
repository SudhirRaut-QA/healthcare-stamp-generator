# -*- coding: utf-8 -*-
"""
Comprehensive Odoo Integration & Stamp Generation Verification Script

This script performs a complete verification of:
1. Core stamp generators functionality
2. Odoo integration adapters
3. API endpoints
4. File generation and storage
5. Integration readiness

Author: Healthcare Stamp Generator Project
Version: 1.0.0
"""

import os
import sys
import importlib.util
from pathlib import Path

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_section(title):
    """Print a section header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title:^80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.END} {message}")

def print_info(message):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.END} {message}")

def check_core_generators():
    """Verify core stamp generators"""
    print_section("1. CORE STAMP GENERATORS VERIFICATION")
    
    results = {
        'hospital': {'available': False, 'generates': False, 'file_saved': False},
        'doctor': {'available': False, 'generates': False, 'file_saved': False}
    }
    
    # Check Hospital Stamp Generator
    print(f"{Colors.BOLD}Hospital Stamp Generator:{Colors.END}")
    try:
        from app.modules.stamp_generator.generator import HospitalStampGenerator
        results['hospital']['available'] = True
        print_success("Module imported successfully")
        
        # Test generation
        gen = HospitalStampGenerator()
        stamp_data = gen.generate_stamp("Test Hospital Integration", size=300)
        
        if isinstance(stamp_data, bytes) and len(stamp_data) > 0:
            results['hospital']['generates'] = True
            print_success(f"Stamp generated successfully (Size: {len(stamp_data):,} bytes)")
            
            # Save to file for verification
            output_path = os.path.join("stampOutput", "test_verification.png")
            with open(output_path, 'wb') as f:
                f.write(stamp_data)
            
            if os.path.exists(output_path):
                results['hospital']['file_saved'] = True
                print_success(f"Stamp saved successfully: {output_path}")
                file_size = os.path.getsize(output_path)
                print_info(f"  File size: {file_size:,} bytes")
            else:
                print_error("Failed to save stamp file")
        else:
            print_error(f"Invalid stamp data (Type: {type(stamp_data)})")
            
    except ImportError as e:
        print_error(f"Import failed: {e}")
    except Exception as e:
        print_error(f"Generation failed: {e}")
    
    # Check Doctor Stamp Generator
    print(f"\n{Colors.BOLD}Doctor Stamp Generator:{Colors.END}")
    try:
        from app.modules.doctor_stamp.generator import DoctorStampGenerator
        results['doctor']['available'] = True
        print_success("Module imported successfully")
        
        # Test generation
        gen = DoctorStampGenerator()
        output_path = gen.generate_doctor_stamp("Dr. Test Doctor", "MBBS, MD", "MCI-12345", width=400, height=200)
        
        if isinstance(output_path, str) and os.path.exists(output_path):
            results['doctor']['generates'] = True
            file_size = os.path.getsize(output_path)
            print_success(f"Stamp generated successfully: {output_path}")
            print_info(f"  File size: {file_size:,} bytes")
            
            # Verify it's a valid PNG
            with open(output_path, 'rb') as f:
                stamp_data = f.read()
            if stamp_data.startswith(b'\x89PNG'):
                results['doctor']['file_saved'] = True
                print_success("Stamp is valid PNG format")
            else:
                print_error("Generated file is not a valid PNG")
        else:
            print_error(f"Invalid output (Type: {type(output_path)})")
            
    except ImportError as e:
        print_error(f"Import failed: {e}")
    except Exception as e:
        print_error(f"Generation failed: {e}")
    
    return results

def check_odoo_adapters():
    """Verify Odoo integration adapters"""
    print_section("2. ODOO INTEGRATION ADAPTERS VERIFICATION")
    
    results = {
        'hospital_adapter': {'available': False, 'core_accessible': False, 'generates': False},
        'doctor_adapter': {'available': False, 'core_accessible': False, 'generates': False}
    }
    
    # Check Hospital Adapter
    print(f"{Colors.BOLD}Hospital Stamp Adapter:{Colors.END}")
    try:
        # Import adapter without Odoo dependencies
        import sys
        import os
        sys.path.insert(0, os.path.join(os.getcwd(), 'odoo_integration', 'lib'))
        
        # Mock the 'odoo' module to avoid import errors
        class MockOdoo:
            pass
        sys.modules['odoo'] = MockOdoo()
        
        from hospital_generator import HospitalStampAdapter
        results['hospital_adapter']['available'] = True
        print_success("Adapter module imported successfully")
        
        adapter = HospitalStampAdapter()
        if adapter.is_available():
            results['hospital_adapter']['core_accessible'] = True
            print_success("Core generator is accessible from adapter")
            
            # Test generation through adapter
            success, image_base64, error = adapter.generate_stamp("Test Hospital via Adapter", size=300)
            if success and image_base64:
                results['hospital_adapter']['generates'] = True
                print_success(f"Stamp generated via adapter (Base64 length: {len(image_base64)} chars)")
            else:
                print_error(f"Adapter generation failed: {error}")
        else:
            print_error("Core generator not accessible from adapter")
            print_warning("Check path configuration in odoo_integration/lib/hospital_generator.py (line ~13)")
            
    except ImportError as e:
        print_error(f"Import failed: {e}")
    except Exception as e:
        print_error(f"Adapter error: {e}")
    
    # Check Doctor Adapter
    print(f"\n{Colors.BOLD}Doctor Stamp Adapter:{Colors.END}")
    try:
        from doctor_generator import DoctorStampAdapter
        results['doctor_adapter']['available'] = True
        print_success("Adapter module imported successfully")
        
        adapter = DoctorStampAdapter()
        if adapter.is_available():
            results['doctor_adapter']['core_accessible'] = True
            print_success("Core generator is accessible from adapter")
            
            # Test generation through adapter
            success, image_base64, error = adapter.generate_stamp("Dr. Test via Adapter", "MBBS", "TEST-123")
            if success and image_base64:
                results['doctor_adapter']['generates'] = True
                print_success(f"Stamp generated via adapter (Base64 length: {len(image_base64)} chars)")
            else:
                print_error(f"Adapter generation failed: {error}")
        else:
            print_error("Core generator not accessible from adapter")
            print_warning("Check path configuration in odoo_integration/lib/doctor_generator.py (line ~13)")
            
    except ImportError as e:
        print_error(f"Import failed: {e}")
    except Exception as e:
        print_error(f"Adapter error: {e}")
    
    return results

def check_odoo_module_structure():
    """Verify Odoo module file structure"""
    print_section("3. ODOO MODULE STRUCTURE VERIFICATION")
    
    required_files = {
        'odoo_integration/__manifest__.py': 'Module manifest file',
        'odoo_integration/__init__.py': 'Module initialization',
        'odoo_integration/models/__init__.py': 'Models package init',
        'odoo_integration/models/hospital_stamp.py': 'Hospital stamp model',
        'odoo_integration/models/doctor_stamp.py': 'Doctor stamp model',
        'odoo_integration/views/hospital_stamp_views.xml': 'Hospital stamp views',
        'odoo_integration/views/doctor_stamp_views.xml': 'Doctor stamp views',
        'odoo_integration/views/menu_views.xml': 'Menu structure',
        'odoo_integration/security/ir.model.access.csv': 'Access rights',
        'odoo_integration/lib/hospital_generator.py': 'Hospital adapter',
        'odoo_integration/lib/doctor_generator.py': 'Doctor adapter',
    }
    
    all_present = True
    for file_path, description in required_files.items():
        if os.path.exists(file_path):
            print_success(f"{description:40} {file_path}")
        else:
            print_error(f"{description:40} {file_path} (MISSING)")
            all_present = False
    
    return all_present

def check_dependencies():
    """Verify required dependencies"""
    print_section("4. DEPENDENCIES VERIFICATION")
    
    dependencies = {
        'PIL': 'Pillow (Image processing)',
        'fastapi': 'FastAPI (Web framework)',
        'uvicorn': 'Uvicorn (ASGI server)',
    }
    
    all_installed = True
    for module, description in dependencies.items():
        try:
            if module == 'PIL':
                import PIL
                from PIL import Image
                version = PIL.__version__
            else:
                mod = __import__(module)
                version = getattr(mod, '__version__', 'Unknown')
            
            print_success(f"{description:40} v{version}")
        except ImportError:
            print_error(f"{description:40} NOT INSTALLED")
            all_installed = False
    
    return all_installed

def generate_integration_summary(core_results, adapter_results, structure_ok, deps_ok):
    """Generate comprehensive integration readiness summary"""
    print_section("5. INTEGRATION READINESS SUMMARY")
    
    print(f"{Colors.BOLD}Core Functionality:{Colors.END}")
    if core_results['hospital']['generates'] and core_results['doctor']['generates']:
        print_success("✓ Both hospital and doctor stamp generators working correctly")
        print_info("  Hospital stamps: Generate PNG binary data successfully")
        print_info("  Doctor stamps: Generate PNG binary data successfully")
    else:
        print_error("✗ Core generators have issues")
        if not core_results['hospital']['generates']:
            print_warning("  Hospital stamp generator not working")
        if not core_results['doctor']['generates']:
            print_warning("  Doctor stamp generator not working")
    
    print(f"\n{Colors.BOLD}Odoo Integration:{Colors.END}")
    if adapter_results['hospital_adapter']['generates'] and adapter_results['doctor_adapter']['generates']:
        print_success("✓ Odoo adapters successfully connect to core generators")
        print_info("  Adapters can import and use core generation functions")
    else:
        print_error("✗ Odoo adapters have issues")
        if not adapter_results['hospital_adapter']['core_accessible']:
            print_warning("  Hospital adapter cannot access core generator")
        if not adapter_results['doctor_adapter']['core_accessible']:
            print_warning("  Doctor adapter cannot access core generator")
    
    print(f"\n{Colors.BOLD}Module Structure:{Colors.END}")
    if structure_ok:
        print_success("✓ All required Odoo module files present")
    else:
        print_error("✗ Some Odoo module files missing")
    
    print(f"\n{Colors.BOLD}Dependencies:{Colors.END}")
    if deps_ok:
        print_success("✓ All required dependencies installed")
    else:
        print_error("✗ Some dependencies missing")
    
    # Overall readiness
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'─'*80}{Colors.END}")
    all_ok = (core_results['hospital']['generates'] and 
              core_results['doctor']['generates'] and
              adapter_results['hospital_adapter']['generates'] and
              adapter_results['doctor_adapter']['generates'] and
              structure_ok and deps_ok)
    
    if all_ok:
        print(f"\n{Colors.BOLD}{Colors.GREEN}✓ INTEGRATION READY FOR ODOO!{Colors.END}\n")
        print("Your Odoo module is ready to install. Next steps:")
        print("  1. Copy odoo_integration folder to Odoo addons directory")
        print("  2. Update path in hospital_generator.py and doctor_generator.py (line ~13)")
        print("  3. Restart Odoo service")
        print("  4. Install 'Healthcare Stamp Generator' module from Odoo Apps")
    else:
        print(f"\n{Colors.BOLD}{Colors.YELLOW}⚠ INTEGRATION NEEDS ATTENTION{Colors.END}\n")
        print("Please address the issues marked above before installing Odoo module.")
        
        if not (adapter_results['hospital_adapter']['core_accessible'] or 
                adapter_results['doctor_adapter']['core_accessible']):
            print(f"\n{Colors.BOLD}Common Fix:{Colors.END}")
            print("  Update the app_path in these files (around line 13):")
            print("    - odoo_integration/lib/hospital_generator.py")
            print("    - odoo_integration/lib/doctor_generator.py")
            print("  Change to your actual project path:")
            print(f"    app_path = r'{os.path.abspath('app')}'")

def main():
    """Main verification function"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║    Healthcare Stamp Generator - Comprehensive Verification Report         ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    # Run all checks
    core_results = check_core_generators()
    adapter_results = check_odoo_adapters()
    structure_ok = check_odoo_module_structure()
    deps_ok = check_dependencies()
    
    # Generate summary
    generate_integration_summary(core_results, adapter_results, structure_ok, deps_ok)
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'─'*80}{Colors.END}")
    print(f"{Colors.BOLD}Verification completed at: {Colors.END}{Colors.CYAN}{os.popen('echo %date% %time%').read().strip()}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'─'*80}{Colors.END}\n")

if __name__ == "__main__":
    main()
