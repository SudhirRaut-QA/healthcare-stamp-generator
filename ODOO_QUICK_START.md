# 🚀 ODOO INTEGRATION - QUICK REFERENCE

## ⚡ FASTEST PATH TO INTEGRATION (15 Minutes)

### 1️⃣ **COPY MODULE** (2 minutes)
```bash
# Linux/Mac
cp -r odoo_integration /path/to/odoo/addons/healthcare_stamp

# Windows PowerShell
Copy-Item "odoo_integration" -Destination "C:\path\to\odoo\addons\healthcare_stamp" -Recurse
```

### 2️⃣ **UPDATE PATH CONFIGURATION** (3 minutes)
⚠️ **MOST IMPORTANT STEP** - Update path to your core generator

**Files to edit:**
1. `healthcare_stamp/lib/hospital_generator.py` (line 13)
2. `healthcare_stamp/lib/doctor_generator.py` (line 13)

**What to change:**
```python
# Find this line (around line 13):
app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'app')

# Replace with YOUR actual path:
app_path = '/path/to/your/healthcare-stamp-generator/app'
```

**Examples:**
```python
# Linux/Mac:
app_path = '/opt/healthcare-stamp-generator/app'

# Windows:
app_path = r'C:\Users\YourName\healthcare-stamp-generator\app'

# Development (if cloned from GitHub):
app_path = r'C:\Projects\healthcare-stamp-generator\app'
```

> 💡 **Tip**: The files already have helpful comments showing where to make changes!

### 3️⃣ **INSTALL DEPENDENCIES** (2 minutes)
```bash
# Ensure Pillow is installed in Odoo's Python environment
pip install Pillow

# If using Odoo's virtual environment:
source /path/to/odoo/venv/bin/activate  # Linux/Mac
# or
c:\odoo\venv\Scripts\activate.ps1  # Windows PowerShell
pip install Pillow
```

### 4️⃣ **UPDATE MANIFEST** (1 minute)
✅ **Already Done!** The manifest file is pre-configured with optional files commented out.

The manifest in `healthcare_stamp/__manifest__.py` is already set up correctly:
```python
'data': [
    'security/ir.model.access.csv',
    # 'data/demo_data.xml',  # Already commented
    'views/menu_views.xml',
    'views/hospital_stamp_views.xml',
    'views/doctor_stamp_views.xml',
    # 'wizard/stamp_wizard_views.xml',  # Already commented
],
```

### 5️⃣ **RESTART ODOO** (2 minutes)
```bash
# Linux
sudo systemctl restart odoo

# Windows Service
Restart-Service Odoo
# OR if running manually: Ctrl+C then restart
```

### 5️⃣ **INSTALL IN ODOO** (2 minutes)
1. Login → **Apps**
2. Click **Update Apps List**
3. Remove "Apps" filter
4. Search: **"Healthcare Stamp"**
5. Click **Activate**

### 6️⃣ **TEST** (1 minute)
1. **Healthcare** → **Hospital Stamps**
2. Click **Create**
3. Name: `"City General Hospital"`
4. Size: `300`
5. Click **Generate Stamp**
6. **Download** and verify!

---

## 📁 FILE LOCATIONS REFERENCE

| Component | Location |
|-----------|----------|
| **Odoo Module** | `C:\Program Files\Odoo\server\addons\healthcare_stamp\` |
| **Core Generator** | `c:\Users\1000040225\...\development\app\` |
| **Hospital Model** | `healthcare_stamp\models\hospital_stamp.py` |
| **Adapter** | `healthcare_stamp\lib\hospital_generator.py` |
| **Views** | `healthcare_stamp\views\*.xml` |
| **Config** | `C:\Program Files\Odoo\server\odoo.conf` |

---

## 🎛️ SPACING CONTROLS

**Location:** `app/modules/stamp_generator/generator.py` (lines 309-313)

```python
BASE_COVERAGE_ANGLE = 330      # Circle usage (270-350)
WORD_GAP_SIZE = 8              # Word spacing (4-15)
MIN_CHAR_SPACING = 4.0         # Min spacing (3-8)
```

**To adjust:**
1. Edit values
2. Restart Odoo
3. Regenerate stamps

---

## 🔧 COMMON CUSTOMIZATIONS

### Add Hospital Logo
```python
# In hospital_stamp.py
logo_field = fields.Binary('Hospital Logo')

# Pass to generator
stamp_bytes = adapter.generate_stamp(
    hospital_name=self.name,
    size=self.size,
    include_logo=True
)
```

### Auto-Generate on Partner Save
```python
# In res.partner (your Odoo customization)
class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def create(self, vals):
        partner = super().create(vals)
        if partner.is_company:  # Only for hospitals
            self.env['healthcare.hospital.stamp'].create({
                'name': partner.name,
                'partner_id': partner.id,
            }).action_generate_stamp()
        return partner
```

### Batch Generation
```python
# Create wizard: wizard/batch_stamp_wizard.py
class BatchStampWizard(models.TransientModel):
    _name = 'batch.stamp.wizard'
    
    def generate_all_hospital_stamps(self):
        partners = self.env['res.partner'].search([
            ('is_company', '=', True)
        ])
        for partner in partners:
            # Generate stamp for each
            pass
```

---

## 🆘 TROUBLESHOOTING QUICK FIXES

| Problem | Quick Fix |
|---------|-----------|
| **Module not visible** | Apps → Update Apps List |
| **Import error PIL** | `pip install Pillow` |
| **Core import failed** | Check adapter path (absolute) |
| **Permission denied** | Run Odoo as administrator |
| **Text overlapping** | Adjust `WORD_GAP_SIZE` |
| **Text past dot** | Decrease `BASE_COVERAGE_ANGLE` |

---

## 📞 SUPPORT RESOURCES

- **Full Guide:** `ODOO_INTEGRATION_STEPS.md`
- **Verification Script:** `python verify_odoo_integration.py`
- **Integration Guide:** `odoo_integration/INTEGRATION_GUIDE.md`
- **Module README:** `odoo_integration/README.md`

---

## ✅ VERIFICATION CHECKLIST

```
□ Module copied to Odoo addons
□ Adapter paths updated (absolute paths)
□ Manifest updated (missing files commented)
□ Odoo service restarted
□ Module installed in Odoo Apps
□ Test stamp generated successfully
□ Stamp downloaded and verified
□ Integration with partners/employees working
```

---

## 🎯 PRODUCTION DEPLOYMENT

```bash
# 1. Copy to production server
scp -r healthcare_stamp user@prod:/opt/odoo/addons/

# 2. Set permissions
sudo chown -R odoo:odoo /opt/odoo/addons/healthcare_stamp
sudo chmod -R 755 /opt/odoo/addons/healthcare_stamp

# 3. Update odoo.conf
# Add path if using custom addons
addons_path = /opt/odoo/addons,/opt/odoo/custom-addons

# 4. Restart
sudo systemctl restart odoo

# 5. Install via UI
# Apps → Update → Search → Install
```

---

**Total Integration Time: ~15 minutes** ⚡
