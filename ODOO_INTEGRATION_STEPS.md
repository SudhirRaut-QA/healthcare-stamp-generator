# 🏥 Hospital Stamp Generator - Odoo Integration Guide

## 📋 **Current Status**

✅ **Already Completed:**
- Odoo module structure exists in `odoo_integration/` folder
- Models created (`hospital_stamp.py`, `doctor_stamp.py`)
- Adapter classes created (`hospital_generator.py`, `doctor_generator.py`)
- Views configured (XML files)
- Manifest file (`__manifest__.py`) ready
- Security rules defined
- Core stamp generator with **NEW simple spacing system**

## 🚀 **Integration Steps**

### **Step 1: Prepare Your Odoo Environment**

#### 1.1 Verify Prerequisites
```bash
# Check Python version (3.8+ required)
python --version

# Ensure Pillow is installed in Odoo environment
pip install Pillow

# Optional: If using separate Odoo Python environment
source /path/to/odoo/venv/bin/activate  # Linux/Mac
# OR
c:\odoo\venv\Scripts\activate.ps1  # Windows
pip install Pillow
```

#### 1.2 Locate Your Odoo Addons Directory
Common paths:
- **Linux**: `/opt/odoo/addons/` or `/usr/lib/python3/dist-packages/odoo/addons/`
- **Windows**: `C:\Program Files\Odoo\server\addons\` or custom path
- **Docker**: Volume mount location
- **Development**: `~/odoo/addons/` or your custom addons path

```bash
# Find your odoo.conf to check addons_path
cat /etc/odoo/odoo.conf | grep addons_path
# OR on Windows
type "C:\Program Files\Odoo\server\odoo.conf" | findstr addons_path
```

---

### **Step 2: Copy Module to Odoo**

#### Option A: Direct Copy (Recommended)
```bash
# Linux/Mac
cp -r "c:/Users/1000040225/OneDrive - Air Canada/Automation scripts/Learning/development/odoo_integration" /path/to/odoo/addons/healthcare_stamp

# Windows PowerShell
Copy-Item "c:\Users\1000040225\OneDrive - Air Canada\Automation scripts\Learning\development\odoo_integration" -Destination "C:\path\to\odoo\addons\healthcare_stamp" -Recurse
```

#### Option B: Symbolic Link (For Development)
```bash
# Linux/Mac
ln -s "c:/Users/1000040225/OneDrive - Air Canada/Automation scripts/Learning/development/odoo_integration" /path/to/odoo/addons/healthcare_stamp

# Windows PowerShell (Run as Administrator)
New-Item -ItemType SymbolicLink -Path "C:\path\to\odoo\addons\healthcare_stamp" -Target "c:\Users\1000040225\OneDrive - Air Canada\Automation scripts\Learning\development\odoo_integration"
```

---

### **Step 3: Copy Core Generator Libraries**

The Odoo module needs access to your core stamp generator. **Choose one option:**

#### **Option 1: Update Adapter Path (Recommended - Simpler)**

Update both adapter files to point to your project location:

**Files to edit:**
- `odoo_integration/lib/hospital_generator.py` (line 13)
- `odoo_integration/lib/doctor_generator.py` (line 13)

**Change this line:**
```python
app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'app')
```

**To your actual project path:**
```python
# Linux/Mac example:
app_path = '/opt/healthcare-stamp-generator/app'

# Windows example:
app_path = r'C:\healthcare-stamp-generator\app'

# Your specific path:
app_path = r'C:\Users\1000040225\OneDrive - Air Canada\Automation scripts\Learning\development\app'
```

> ⚠️ **IMPORTANT**: The files already have helpful comments. Just uncomment and update the path!

#### **Option 2: Copy Core Libraries (Self-Contained)**

```bash
# Copy entire app folder into Odoo module
mkdir /path/to/odoo/addons/healthcare_stamp/core
cp -r app/* /path/to/odoo/addons/healthcare_stamp/core/

# Update imports in both adapters to use local copy
# In hospital_generator.py and doctor_generator.py, change:
from modules.stamp_generator.generator import HospitalStampGenerator
# To:
from core.modules.stamp_generator.generator import HospitalStampGenerator
```

---

### **Step 4: Update Odoo Module Manifest**

The manifest needs some adjustments for missing files:

```python
# Edit: odoo_integration/__manifest__.py

'data': [
    'security/ir.model.access.csv',
    # 'data/demo_data.xml',  # Comment out if file missing
    'views/menu_views.xml',
    'views/hospital_stamp_views.xml',
    'views/doctor_stamp_views.xml',
    # 'wizard/stamp_wizard_views.xml',  # Comment out if not created yet
],
'demo': [
    # 'data/demo_data.xml',  # Comment out if file missing
],
'qweb': [
    # 'static/src/xml/stamp_templates.xml',  # Comment out if not created yet
],
```

---

### **Step 5: Install Module in Odoo**

#### 5.1 Restart Odoo Service
```bash
# Linux
sudo systemctl restart odoo

# Windows Service
Restart-Service Odoo

# Development Mode (if running manually)
# Stop current server (Ctrl+C)
# Start with update flag
./odoo-bin -u healthcare_stamp -d your_database_name
```

#### 5.2 Install via Odoo UI
1. **Login** to Odoo as Administrator
2. Navigate to **Apps** menu
3. Click **Update Apps List** (removes filter)
4. **Search** for "Healthcare Stamp Generator"
5. Click **Activate/Install**

![Odoo Install Screenshot]
```
Apps → Update Apps List → Search "Healthcare Stamp" → Install
```

#### 5.3 Verify Installation
Check Odoo logs for any errors:
```bash
# Linux
tail -f /var/log/odoo/odoo-server.log

# Windows
# Check: C:\Program Files\Odoo\server\odoo.log
```

---

### **Step 6: Configure Module Settings**

#### 6.1 Set File Permissions (Linux Only)
```bash
# Ensure Odoo can read/write stamp files
sudo chown -R odoo:odoo /path/to/odoo/addons/healthcare_stamp
sudo chmod -R 755 /path/to/odoo/addons/healthcare_stamp
```

#### 6.2 Configure Output Folder
```python
# In hospital_stamp.py model, update output path if needed
def _get_stamp_output_path(self):
    """Get output path for generated stamps"""
    # Default: stores in Odoo filestore
    return os.path.join(self.env['ir.attachment']._filestore(), 'stamps')
```

---

### **Step 7: Test the Integration**

#### 7.1 Create Hospital Stamp Record
1. Navigate to **Healthcare → Hospital Stamps**
2. Click **Create**
3. Enter hospital name: `"City General Hospital"`
4. Set size: `300`
5. Click **Save**
6. Click **Generate Stamp** button
7. Download generated stamp

#### 7.2 Test Doctor Stamp
1. Navigate to **Healthcare → Doctor Stamps**
2. Click **Create**
3. Enter details:
   - Name: `"Dr. Sarah Johnson"`
   - Degree: `"MBBS, MD (Cardiology)"`
   - Registration: `"Reg. No: MCI-12345"`
4. Click **Generate Stamp**
5. Download result

#### 7.3 Verify Generated Files
```bash
# Check if stamps are being created
ls -la /path/to/odoo/addons/healthcare_stamp/stampOutput/
# OR check Odoo filestore
ls -la /path/to/odoo/.local/share/Odoo/filestore/your_db/stamps/
```

---

### **Step 8: Integration with Existing Odoo Apps**

#### 8.1 Link with Hospital Partners
```python
# In your existing hospital model (e.g., res.partner)
class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    hospital_stamp_ids = fields.One2many(
        'healthcare.hospital.stamp', 
        'partner_id', 
        string='Hospital Stamps'
    )
    
    def action_generate_hospital_stamp(self):
        """Quick action to generate stamp for this hospital"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Generate Hospital Stamp',
            'res_model': 'healthcare.hospital.stamp',
            'view_mode': 'form',
            'context': {
                'default_name': self.name,
                'default_partner_id': self.id,
            },
            'target': 'new',
        }
```

#### 8.2 Add to Employee Records
```python
# In hr.employee
class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    doctor_stamp_ids = fields.One2many(
        'healthcare.doctor.stamp',
        'employee_id',
        string='Doctor Stamps'
    )
    
    # Add medical fields
    medical_degree = fields.Char('Medical Degree')
    registration_number = fields.Char('Medical Registration Number')
    specialization = fields.Char('Medical Specialization')
```

#### 8.3 Use in Reports
```xml
<!-- In your Qweb report template -->
<template id="report_prescription">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="prescription">
            <div class="page">
                <h2>Medical Prescription</h2>
                
                <!-- Doctor Stamp -->
                <t t-if="prescription.doctor_id.doctor_stamp_ids">
                    <t t-set="stamp" t-value="prescription.doctor_id.doctor_stamp_ids[0]"/>
                    <img t-att-src="'data:image/png;base64,%s' % stamp.stamp_image" 
                         style="width: 200px; height: 100px;"/>
                </t>
                
                <!-- Hospital Stamp -->
                <t t-if="prescription.hospital_id.hospital_stamp_ids">
                    <t t-set="h_stamp" t-value="prescription.hospital_id.hospital_stamp_ids[0]"/>
                    <img t-att-src="'data:image/png;base64,%s' % h_stamp.stamp_image"
                         style="width: 150px; height: 150px;"/>
                </t>
            </div>
        </t>
    </t>
</template>
```

---

### **Step 9: Customize Spacing Controls**

Your new **simple spacing system** allows easy customization:

#### Update Hospital Stamp Generator
```python
# In generator.py, adjust manual controls (lines 309-313)
BASE_COVERAGE_ANGLE = 330      # How much of circle to use (270-350)
WORD_GAP_SIZE = 8              # Degrees between words (4-15)
MIN_CHAR_SPACING = 4.0         # Minimum spacing (3.0-8.0)
```

#### Expose in Odoo UI (Optional)
```python
# In healthcare.hospital.stamp model
class HospitalStamp(models.Model):
    _name = 'healthcare.hospital.stamp'
    
    # Add spacing controls
    coverage_angle = fields.Integer('Coverage Angle', default=330)
    word_gap = fields.Integer('Word Gap', default=8)
    min_char_spacing = fields.Float('Min Character Spacing', default=4.0)
    
    def _generate_hospital_stamp_image(self):
        """Pass custom spacing to generator"""
        from lib.hospital_generator import HospitalStampAdapter
        
        adapter = HospitalStampAdapter()
        stamp_bytes = adapter.generate_stamp(
            hospital_name=self.name,
            size=self.size,
            coverage_angle=self.coverage_angle,
            word_gap=self.word_gap,
            min_char_spacing=self.min_char_spacing
        )
        return base64.b64encode(stamp_bytes)
```

---

### **Step 10: API Access (External Systems)**

#### 10.1 Enable API Access
```python
# In your Odoo configuration
[options]
# ...
xmlrpc = True
xmlrpc_interface = 0.0.0.0
xmlrpc_port = 8069
```

#### 10.2 Use from External Applications
```python
# Example: Python client
import xmlrpc.client

url = 'http://your-odoo-server:8069'
db = 'your_database'
username = 'admin'
password = 'admin_password'

# Authenticate
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

# Create stamp
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
stamp_id = models.execute_kw(db, uid, password,
    'healthcare.hospital.stamp', 'create',
    [{'name': 'City General Hospital', 'size': 300}]
)

# Generate stamp
models.execute_kw(db, uid, password,
    'healthcare.hospital.stamp', 'action_generate_stamp',
    [[stamp_id]]
)

# Download stamp
stamp_data = models.execute_kw(db, uid, password,
    'healthcare.hospital.stamp', 'read',
    [[stamp_id]], {'fields': ['stamp_image', 'stamp_filename']}
)
print(stamp_data)
```

---

## 🎯 **Quick Checklist**

- [ ] **Prerequisites installed** (Python 3.8+, Pillow)
- [ ] **Module copied** to Odoo addons directory
- [ ] **Core libraries** accessible (path updated or copied)
- [ ] **Manifest updated** (commented out missing files)
- [ ] **Odoo service restarted**
- [ ] **Module installed** via Odoo Apps
- [ ] **Permissions set** (Linux only)
- [ ] **Test stamp generated** successfully
- [ ] **Integration tested** with partners/employees
- [ ] **Reports configured** (if needed)

---

## 🆘 **Troubleshooting**

### Issue 1: "Module not found in Apps"
**Solution:** 
- Update Apps List in Odoo
- Check addons_path in odoo.conf
- Restart Odoo service

### Issue 2: "PIL/Pillow import error"
**Solution:**
```bash
# Ensure Pillow in Odoo environment
source /path/to/odoo/venv/bin/activate
pip install Pillow
sudo systemctl restart odoo
```

### Issue 3: "Core generator import failed"
**Solution:**
- Update adapter path in `lib/hospital_generator.py`
- OR copy core libraries into module
- Check Python path in Odoo logs

### Issue 4: "Permission denied creating stamps"
**Solution:**
```bash
sudo chown -R odoo:odoo /path/to/odoo/addons/healthcare_stamp
sudo chmod -R 755 /path/to/odoo/addons/healthcare_stamp
```

### Issue 5: "Stamp text overlapping/messy"
**Solution:**
- Adjust manual controls in `generator.py`:
  ```python
  BASE_COVERAGE_ANGLE = 330  # Increase/decrease
  WORD_GAP_SIZE = 8          # Adjust gap
  MIN_CHAR_SPACING = 4.0     # Prevent overlap
  ```

---

## 📚 **Additional Resources**

- **Full Integration Guide**: `odoo_integration/INTEGRATION_GUIDE.md`
- **Odoo Module README**: `odoo_integration/README.md`
- **Doctor Stamp Guide**: `DOCTOR_STAMP_GUIDE.md`
- **Usage Examples**: `USAGE_EXAMPLES.md`
- **API Documentation**: Run FastAPI server and visit `http://localhost:8000/docs`

---

## 🎉 **Success!**

Once completed, you'll have:
- ✅ Stamps accessible from **Healthcare menu**
- ✅ Integration with **Partners** (hospitals)
- ✅ Integration with **Employees** (doctors)
- ✅ **Report integration** for medical documents
- ✅ **API access** for external systems
- ✅ **Customizable spacing** via simple controls

**Next Steps:**
1. Customize stamp appearance for your hospital branding
2. Create batch generation wizards
3. Add automated stamp generation on record creation
4. Integrate with patient management system
5. Add stamp approval workflows

---

**Need Help?** Check the detailed guides in the `odoo_integration/` folder or create an issue on GitHub.
