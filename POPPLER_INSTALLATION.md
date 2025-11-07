# PDF Processing Notice

## Poppler Installation Required for PDF Preview

The document stamping system requires **Poppler** to process PDF files and generate previews. Currently, Poppler is not installed on your system.

### What This Means:
- ✅ **Image files** (PNG, JPG, JPEG, BMP, TIFF) work perfectly
- ✅ **PDF stamping** still works (stamps can be added)
- ⚠️ **PDF preview** shows placeholder images instead of actual content
- ⚠️ **PDF processing** uses fallback methods

### Quick Installation Options:

#### Option 1: Chocolatey (Recommended for Windows)
```powershell
# Install Chocolatey if not already installed
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install Poppler
choco install poppler
```

#### Option 2: Manual Installation
1. Download Poppler for Windows: https://github.com/oschwartz10612/poppler-windows/releases
2. Extract the ZIP file
3. Add the `bin` folder to your system PATH
4. Restart your command prompt/IDE

#### Option 3: Conda (if using Anaconda/Miniconda)
```bash
conda install -c conda-forge poppler
```

#### Option 4: Use Pre-built Wheels
```bash
pip install pdf2image
# Then follow manual installation above for Poppler binaries
```

### Verification:
After installation, verify Poppler is working:
```bash
pdftoppm -h
```

### Alternative Solution:
If you only need to work with image files (PNG, JPG, etc.), the system works perfectly without Poppler. Simply upload image files instead of PDFs.

### Need Help?
Run the installation helper:
```bash
python install_poppler.py
```

---
**Note**: The document stamping system will automatically detect when Poppler becomes available and switch to full PDF processing mode.