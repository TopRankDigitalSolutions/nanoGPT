# Google Cloud Vision OCR Setup

## Quick Setup

### 1. Python Dependencies (Already Installed)
```bash
pip install google-cloud-vision pdf2image pillow
```

### 2. Google Cloud Account
1. Go to https://console.cloud.google.com/
2. Create new project (or select existing)
3. Enable Vision API:
   - APIs & Services → Library
   - Search "Cloud Vision API" → Enable

### 3. Authentication (Choose One)

#### Option A: Service Account (Recommended)
1. Go to IAM & Admin → Service Accounts
2. Create Service Account
3. Add Role: "Cloud Vision API User"  
4. Generate JSON key
5. Download and save the key file
6. Set environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your-service-key.json"

# Make it permanent (add to ~/.zshrc or ~/.bashrc)
echo 'export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"' >> ~/.zshrc
```

#### Option B: Application Default Credentials
```bash
# Install Google Cloud CLI
brew install google-cloud-sdk

# Login and authenticate
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

### 4. Test Setup
```bash
python ocr_google_vision.py --test
```

## Usage Examples

### Single PDF
```bash
# Basic OCR
python ocr_google_vision.py document.pdf

# High-quality document OCR (better for complex layouts)
python ocr_google_vision.py document.pdf --detailed

# Custom output directory
python ocr_google_vision.py document.pdf --output ./extracted_text
```

### Batch Processing
```bash
# Process all PDFs in folder
python ocr_google_vision.py /path/to/pdfs/ --batch

# Batch with detailed OCR
python ocr_google_vision.py ./pdfs/ --batch --detailed
```

## Cost Information

### Free Tier
- **1,000 requests per month** for free
- Each page = 1 request

### Paid Pricing
- **$1.50 per 1,000 requests** after free tier
- Very affordable: 10,000 pages = $15

### Cost Control
Set up billing alerts:
1. Google Cloud Console → Billing → Budgets & alerts
2. Create budget with email alerts at $5, $10, etc.

## Features

### Standard vs Detailed OCR
- **Standard** (`--detailed` not used): Fast, good for simple text
- **Detailed** (`--detailed` flag): Slower, better for:
  - Complex layouts
  - Tables and forms  
  - Mixed fonts and sizes
  - Provides confidence scores

### Output Files
The script creates:
- `complete_extracted_text.txt` - All pages combined
- `page_001.txt`, `page_002.txt`, etc. - Individual pages
- `extraction_summary.txt` - Statistics and cost info

## Troubleshooting

### Authentication Errors
```bash
# Check current authentication
gcloud auth list

# Reset authentication  
gcloud auth application-default login

# Verify project
gcloud config get-value project
```

### "Permission Denied" Errors
1. Make sure Vision API is enabled
2. Check service account has "Cloud Vision API User" role
3. Verify JSON key file path is correct

### "Quota Exceeded" Errors
1. Check you haven't exceeded 1,000 free requests
2. Enable billing if you need more requests
3. Set up quotas to control costs

## Example Output
```
🔍 Processing PDF: document.pdf  
📁 Output directory: google_vision_extracted
📊 Mode: Detailed Document OCR

📄 Converting PDF to images (DPI: 300)...
✅ Converted 3 pages

🔄 Processing page 1/3...
✅ Page 1: 1,247 chars, 234 words, confidence: 95.2%

🔄 Processing page 2/3...  
✅ Page 2: 1,156 chars, 198 words, confidence: 92.8%

🎉 EXTRACTION COMPLETE!
📊 Statistics:
   • Pages processed: 3
   • Total characters: 3,678
   • Total words: 645
   • API calls used: 3
   • Average confidence: 94.1%
💰 Cost: $0.0045 (after free 1,000/month)
```

## Comparison with Free Version

| Feature | Free Tesseract | Google Vision |
|---------|----------------|---------------|
| **Cost** | $0 | $1.50/1K pages after free 1K |
| **Setup Time** | 5 minutes | 15 minutes |
| **Quality** | Good | Excellent |
| **Complex Layouts** | Fair | Excellent |
| **Tables/Forms** | Poor | Excellent |
| **Speed** | Slower | Faster |
| **Confidence Scores** | No | Yes |
| **Language Support** | Good | Excellent |
