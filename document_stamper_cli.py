#!/usr/bin/env python3
"""
Interactive Document Stamper CLI
Command-line interface for adding stamps to documents with preview functionality.
"""

import os
import sys
import argparse
from typing import List, Optional
from PIL import Image

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from modules.document_stamper.document_processor import DocumentProcessor
from modules.document_stamper.stamp_overlay import StampOverlay
from modules.document_stamper.preview_generator import PreviewGenerator
from modules.stamp_generator.generator import HospitalStampGenerator
from modules.doctor_stamp.generator import DoctorStampGenerator

class DocumentStamperCLI:
    """Interactive command-line document stamper."""
    
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.stamp_overlay = StampOverlay()
        self.preview_generator = PreviewGenerator(self.stamp_overlay)
        self.current_document = None
        self.output_dir = "stampedDocuments"
        
        # Create output directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def load_document(self, file_path: str) -> bool:
        """Load a document for stamping."""
        try:
            print(f"📄 Loading document: {file_path}")
            self.current_document = self.document_processor.load_document(file_path)
            
            print(f"✅ Document loaded successfully!")
            print(f"   Type: {self.current_document['document_type']}")
            print(f"   Pages: {self.current_document['page_count']}")
            print(f"   Filename: {self.current_document['metadata']['filename']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to load document: {e}")
            return False
    
    def show_document_info(self):
        """Display document information."""
        if not self.current_document:
            print("❌ No document loaded")
            return
        
        print("\n📋 Document Information:")
        print(f"   File: {self.current_document['metadata']['filename']}")
        print(f"   Type: {self.current_document['document_type']}")
        print(f"   Pages: {self.current_document['page_count']}")
        
        if self.current_document['document_type'] == 'IMAGE':
            page = self.current_document['pages'][0]
            print(f"   Dimensions: {page['width']}x{page['height']}")
        
        # Show stamp summary
        summary = self.stamp_overlay.get_stamps_summary()
        print(f"\n🔖 Stamps Summary:")
        print(f"   Total stamps: {summary['total_stamps']}")
        print(f"   Pages with stamps: {summary['pages_with_stamps']}")
        
        if summary['stamp_types']:
            print("   Stamp types:")
            for stamp_type, count in summary['stamp_types'].items():
                print(f"     {stamp_type}: {count}")
    
    def add_hospital_stamp(self, page_number: int, hospital_name: str, 
                          x: float = 0.5, y: float = 0.5):
        """Add a hospital stamp to a page."""
        if not self.current_document:
            print("❌ No document loaded")
            return False
        
        try:
            print(f"🏥 Generating hospital stamp for: {hospital_name}")
            
            # Generate stamp
            generator = HospitalStampGenerator()
            stamp_bytes = generator.generate_stamp(hospital_name)
            
            # Convert bytes to PIL Image
            from PIL import Image
            from io import BytesIO
            stamp_image = Image.open(BytesIO(stamp_bytes))
            
            # Add to overlay
            stamp_id = self.stamp_overlay.add_stamp(
                page_number=page_number,
                stamp_type='hospital',
                stamp_image=stamp_image,
                stamp_data={'hospital_name': hospital_name, 'type': 'hospital'},
                x=x, y=y
            )
            
            print(f"✅ Hospital stamp added successfully! (ID: {stamp_id[:8]}...)")
            return True
            
        except Exception as e:
            print(f"❌ Failed to add hospital stamp: {e}")
            return False
    
    def add_doctor_stamp(self, page_number: int, doctor_name: str, 
                        degree: str, registration_number: str,
                        x: float = 0.5, y: float = 0.5):
        """Add a doctor stamp to a page."""
        if not self.current_document:
            print("❌ No document loaded")
            return False
        
        try:
            print(f"🩺 Generating doctor stamp for: {doctor_name}")
            
            # Generate stamp
            generator = DoctorStampGenerator()
            stamp_file_path = generator.generate_doctor_stamp(doctor_name, degree, registration_number)
            
            # Load the generated stamp image
            from PIL import Image
            stamp_image = Image.open(stamp_file_path)
            
            # Add to overlay
            stamp_id = self.stamp_overlay.add_stamp(
                page_number=page_number,
                stamp_type='doctor',
                stamp_image=stamp_image,
                stamp_data={
                    'doctor_name': doctor_name,
                    'degree': degree,
                    'registration_number': registration_number,
                    'type': 'doctor'
                },
                x=x, y=y
            )
            
            print(f"✅ Doctor stamp added successfully! (ID: {stamp_id[:8]}...)")
            return True
            
        except Exception as e:
            print(f"❌ Failed to add doctor stamp: {e}")
            return False
    
    def preview_page(self, page_number: int, show_boundaries: bool = False):
        """Generate and save preview of a page."""
        if not self.current_document:
            print("❌ No document loaded")
            return
        
        try:
            page_data = self.document_processor.get_page(page_number)
            if not page_data:
                print(f"❌ Page {page_number} not found")
                return
            
            print(f"🖼️ Generating preview for page {page_number}...")
            
            # Generate preview
            preview_result = self.preview_generator.generate_page_preview(
                page_data['image'],
                page_number,
                preview_width=800,
                show_boundaries=show_boundaries
            )
            
            # Save preview
            filename = f"preview_page_{page_number}.png"
            filepath = os.path.join(self.output_dir, filename)
            preview_result['preview_image'].save(filepath)
            
            print(f"✅ Preview saved: {filepath}")
            print(f"   Dimensions: {preview_result['width']}x{preview_result['height']}")
            print(f"   Stamps on page: {preview_result['stamp_count']}")
            
        except Exception as e:
            print(f"❌ Failed to generate preview: {e}")
    
    def save_stamped_document(self, output_filename: Optional[str] = None):
        """Save the complete stamped document."""
        if not self.current_document:
            print("❌ No document loaded")
            return
        
        try:
            if not output_filename:
                base_name = os.path.splitext(self.current_document['metadata']['filename'])[0]
                output_filename = f"{base_name}_stamped.pdf"
            
            output_path = os.path.join(self.output_dir, output_filename)
            
            print(f"💾 Saving stamped document...")
            
            # Generate stamped pages
            stamped_pages = []
            for i in range(1, self.current_document['page_count'] + 1):
                page_data = self.document_processor.get_page(i)
                preview_result = self.preview_generator.generate_page_preview(
                    page_data['image'], i, show_boundaries=False
                )
                stamped_pages.append(preview_result['preview_image'])
            
            # Save as PDF if multiple pages, otherwise as PNG
            if len(stamped_pages) == 1:
                stamped_pages[0].save(output_path.replace('.pdf', '.png'))
                print(f"✅ Stamped document saved: {output_path.replace('.pdf', '.png')}")
            else:
                # Convert to PDF
                stamped_pages[0].save(
                    output_path, 
                    save_all=True, 
                    append_images=stamped_pages[1:],
                    format='PDF'
                )
                print(f"✅ Stamped document saved: {output_path}")
            
        except Exception as e:
            print(f"❌ Failed to save stamped document: {e}")
    
    def list_stamps(self, page_number: Optional[int] = None):
        """List stamps on a page or all pages."""
        if page_number:
            stamps = self.stamp_overlay.get_page_stamps(page_number)
            print(f"\n🔖 Stamps on page {page_number}:")
            
            if not stamps:
                print("   No stamps on this page")
            else:
                for i, stamp in enumerate(stamps, 1):
                    print(f"   {i}. {stamp.stamp_type.upper()} STAMP")
                    print(f"      Position: {stamp.x:.2f}, {stamp.y:.2f}")
                    print(f"      Size: {stamp.width}x{stamp.height}")
                    print(f"      ID: {stamp.stamp_id[:8]}...")
        else:
            summary = self.stamp_overlay.get_stamps_summary()
            print(f"\n🔖 All Stamps Summary:")
            print(f"   Total stamps: {summary['total_stamps']}")
            print(f"   Pages with stamps: {summary['pages_with_stamps']}")
            
            for page_num, count in summary['pages'].items():
                print(f"   Page {page_num}: {count} stamp(s)")
    
    def clear_stamps(self, page_number: Optional[int] = None):
        """Clear stamps from a page or all pages."""
        if page_number:
            count = self.stamp_overlay.clear_page_stamps(page_number)
            print(f"✅ Cleared {count} stamp(s) from page {page_number}")
        else:
            count = self.stamp_overlay.clear_all_stamps()
            print(f"✅ Cleared {count} stamp(s) from all pages")
    
    def interactive_mode(self):
        """Run interactive stamping session."""
        print("\n🎯 Interactive Document Stamping Mode")
        print("Type 'help' for available commands or 'quit' to exit\n")
        
        while True:
            try:
                command = input("📝 Document Stamper> ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    print("👋 Goodbye!")
                    break
                
                elif command == 'help':
                    self.show_help()
                
                elif command == 'info':
                    self.show_document_info()
                
                elif command.startswith('hospital '):
                    self.handle_hospital_command(command)
                
                elif command.startswith('doctor '):
                    self.handle_doctor_command(command)
                
                elif command.startswith('preview '):
                    page_num = int(command.split()[1]) if len(command.split()) > 1 else 1
                    self.preview_page(page_num)
                
                elif command == 'save':
                    self.save_stamped_document()
                
                elif command.startswith('list'):
                    if len(command.split()) > 1:
                        page_num = int(command.split()[1])
                        self.list_stamps(page_num)
                    else:
                        self.list_stamps()
                
                elif command.startswith('clear'):
                    if len(command.split()) > 1:
                        page_num = int(command.split()[1])
                        self.clear_stamps(page_num)
                    else:
                        self.clear_stamps()
                
                else:
                    print("❓ Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def handle_hospital_command(self, command: str):
        """Handle hospital stamp command."""
        parts = command.split(' ', 2)
        if len(parts) < 3:
            print("❌ Usage: hospital <page_number> <hospital_name>")
            return
        
        try:
            page_num = int(parts[1])
            hospital_name = parts[2]
            self.add_hospital_stamp(page_num, hospital_name)
        except ValueError:
            print("❌ Invalid page number")
    
    def handle_doctor_command(self, command: str):
        """Handle doctor stamp command."""
        print("🩺 Enter doctor stamp details:")
        try:
            page_num = int(input("   Page number: "))
            doctor_name = input("   Doctor name: ").strip()
            degree = input("   Degree: ").strip()
            registration = input("   Registration number: ").strip()
            
            if all([doctor_name, degree, registration]):
                self.add_doctor_stamp(page_num, doctor_name, degree, registration)
            else:
                print("❌ All fields are required")
        except ValueError:
            print("❌ Invalid page number")
    
    def show_help(self):
        """Show help information."""
        print("""
🆘 Available Commands:
   
📋 Document Information:
   info                    - Show document information and stamp summary
   
🔖 Add Stamps:
   hospital <page> <name>  - Add hospital stamp (e.g., hospital 1 "City Hospital")
   doctor                  - Add doctor stamp (interactive input)
   
🖼️ Preview & Save:
   preview [page]          - Generate page preview (default: page 1)
   save                    - Save stamped document
   
📊 Manage Stamps:
   list [page]             - List stamps (all pages or specific page)
   clear [page]            - Clear stamps (all pages or specific page)
   
🚪 Navigation:
   help                    - Show this help
   quit/exit               - Exit the program
   
💡 Examples:
   hospital 1 "General Hospital"
   doctor
   preview 1
   list 1
   clear
        """)

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Interactive Document Stamper - Add stamps to healthcare documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python document_stamper_cli.py prescription.pdf
  python document_stamper_cli.py --hospital "City Hospital" --page 1 invoice.png
  python document_stamper_cli.py --doctor "Dr. Smith" --degree "MBBS" --reg "MCI-123" document.pdf
        """
    )
    
    parser.add_argument('document', help='Path to document file (PDF, PNG, JPG, etc.)')
    parser.add_argument('--hospital', help='Add hospital stamp with given name')
    parser.add_argument('--doctor', help='Doctor name for doctor stamp')
    parser.add_argument('--degree', help='Doctor degree (required with --doctor)')
    parser.add_argument('--registration', '--reg', help='Registration number (required with --doctor)')
    parser.add_argument('--page', type=int, default=1, help='Page number for stamp placement (default: 1)')
    parser.add_argument('--position', help='Stamp position as "x,y" (0.0-1.0, default: 0.5,0.5)')
    parser.add_argument('--preview', action='store_true', help='Generate preview after adding stamps')
    parser.add_argument('--save', help='Save stamped document with given filename')
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    
    args = parser.parse_args()
    
    # Initialize CLI
    cli = DocumentStamperCLI()
    
    # Load document
    if not cli.load_document(args.document):
        return 1
    
    # Parse position
    x, y = 0.5, 0.5
    if args.position:
        try:
            pos_parts = args.position.split(',')
            x, y = float(pos_parts[0]), float(pos_parts[1])
        except (ValueError, IndexError):
            print("❌ Invalid position format. Use 'x,y' with values 0.0-1.0")
            return 1
    
    # Add stamps based on arguments
    if args.hospital:
        cli.add_hospital_stamp(args.page, args.hospital, x, y)
    
    if args.doctor:
        if not args.degree or not args.registration:
            print("❌ Doctor stamps require --degree and --registration arguments")
            return 1
        cli.add_doctor_stamp(args.page, args.doctor, args.degree, args.registration, x, y)
    
    # Generate preview if requested
    if args.preview:
        cli.preview_page(args.page)
    
    # Save document if requested
    if args.save:
        cli.save_stamped_document(args.save)
    
    # Run interactive mode if requested
    if args.interactive or (not args.hospital and not args.doctor):
        cli.interactive_mode()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())