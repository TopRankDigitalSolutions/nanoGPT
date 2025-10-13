# Free OCR Setup - No Cloud Services, No Costs

Extract text from PDF files with scanned images using Tesseract OCR - completely free and runs locally on your machine.

## Quick Install

### 1. Install Python Dependencies
```bash
pip install pytesseract pdf2image pillow opencv-python
```

### 2. Install System Dependencies

**macOS:**
```bash
brew install tesseract poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr poppler-utils
```

**Windows:**
```bash
# Install via conda or download binaries manually
conda install -c conda-forge tesseract poppler
```

### 3. Test Installation
```bash
python ocr_free.py --check
```

## Usage Examples

### Single PDF File
```bash
# Basic usage
python ocr_free.py your_document.pdf

# High quality for small text
python ocr_free.py your_document.pdf --dpi 600

# Debug mode (saves processing steps)
python ocr_free.py your_document.pdf --debug

# Custom output directory
python ocr_free.py your_document.pdf --output ./my_extracted_text
```

### Batch Process Multiple PDFs
```bash
# Process all PDFs in a folder
python ocr_free.py /path/to/pdf_folder/ --batch

# Batch with high DPI
python ocr_free.py ./pdfs/ --batch --dpi 600
```

## What You Get

The script creates a structured output:
```
ocr_free_pdf/
├── document_name/
│   ├── complete_extracted_text.txt    # All pages combined
│   ├── page_001.txt                   # Individual pages
│   ├── page_002.txt
│   ├── ...
│   └── debug_images/                  # Processing steps (if --debug)
│       ├── page_1_01_original.png
│       ├── page_1_02_gray.png
│       └── ...
```

## Advanced Options

### DPI Settings
- **300 DPI**: Good for normal documents (default)
- **600 DPI**: Better for small text or poor quality scans
- **150 DPI**: Faster processing, lower quality

### Debug Mode
Use `--debug` to see how the image preprocessing works:
```bash
python ocr_free.py document.pdf --debug
```

This saves images showing:
1. Original page
2. Grayscale conversion
3. Contrast enhancement
4. Threshold (black/white)
5. Final cleaned image

## Troubleshooting

### "Tesseract not found"
```bash
# macOS
brew install tesseract

# Ubuntu
sudo apt-get install tesseract-ocr

# Check installation
tesseract --version
```

### "Poppler not found" 
```bash
# macOS
brew install poppler

# Ubuntu  
sudo apt-get install poppler-utils
```

### Poor OCR Results
1. **Try higher DPI**: `--dpi 600`
2. **Use debug mode** to see image processing: `--debug`
3. **Check source quality**: Blurry scans will have poor results
4. **Consider preprocessing**: Some documents may need manual cleanup

### Different Languages
```bash
# Install language packs (example for Spanish)
brew install tesseract-lang  # macOS
sudo apt-get install tesseract-ocr-spa  # Ubuntu

# Use in script by modifying the OCR config
# Edit ocr_free.py and add: -l spa to the config strings
```

## Example Output

```
🔍 Processing PDF: document.pdf
📁 Output directory: ocr_free_pdf
📄 Converting PDF to images (DPI: 300)...
✅ Converted 5 pages

🔄 Processing page 1/5...
✅ Page 1: 1,247 chars, confidence: 89.2, time: 2.3s

🔄 Processing page 2/5...
✅ Page 2: 1,156 chars, confidence: 91.5, time: 2.1s

🎉 EXTRACTION COMPLETE!
📊 Statistics:
   • Pages processed: 5
   • Total characters: 6,234
   • Average confidence: 90.1%
   • Combined file: ocr_free_pdf/complete_extracted_text.txt
```

## Cost Comparison

| Solution | Cost | Setup | Quality |
|----------|------|-------|---------|
| **This Free OCR** | $0 | 5 minutes | Good |
| Google Vision API | $1.50/1000 pages | 15 minutes | Excellent |
| Adobe PDF Services | $0.05-0.15/page | Account needed | Excellent |

## Performance Tips

1. **Start with default settings** - works for most documents
2. **Use higher DPI only if needed** - slows processing significantly  
3. **Process in batches** - more efficient for many files
4. **Check debug images** - helps understand processing issues
5. **Clean source PDFs** - better input = better output
