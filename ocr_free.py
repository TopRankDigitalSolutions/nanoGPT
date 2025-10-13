#!/usr/bin/env python3
"""
Free OCR solution using Tesseract with image preprocessing
No cloud services, no costs - runs entirely locally

Requirements:
- pip install pytesseract pdf2image pillow opencv-python
- brew install tesseract poppler (macOS)
- sudo apt-get install tesseract-ocr poppler-utils (Ubuntu)
"""

import cv2
import numpy as np
from pdf2image import convert_from_path
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os
import argparse
import time
from pathlib import Path

def preprocess_image(image, debug_dir=None, page_num=None):
    """
    Enhance image quality for better OCR results
    Returns processed PIL Image
    """
    # Convert PIL to OpenCV format
    opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Save original if debugging
    if debug_dir and page_num is not None:
        cv2.imwrite(f"{debug_dir}/page_{page_num}_01_original.png", opencv_image)
    
    # Convert to grayscale
    gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
    
    # Step 1: Remove noise with median filter
    denoised = cv2.medianBlur(gray, 3)
    
    # Step 2: Enhance contrast with CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(denoised)
    
    # Step 3: Sharpen the image
    kernel = np.array([[-1,-1,-1],
                      [-1, 9,-1],
                      [-1,-1,-1]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)
    
    # Step 4: Threshold for binary image (black text on white background)
    # Try adaptive threshold first (better for varying lighting)
    try:
        thresh = cv2.adaptiveThreshold(
            sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
    except:
        # Fallback to Otsu threshold
        _, thresh = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Step 5: Morphological operations to clean up
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Save processed steps if debugging
    if debug_dir and page_num is not None:
        cv2.imwrite(f"{debug_dir}/page_{page_num}_02_gray.png", gray)
        cv2.imwrite(f"{debug_dir}/page_{page_num}_03_enhanced.png", enhanced)
        cv2.imwrite(f"{debug_dir}/page_{page_num}_04_thresh.png", thresh)
        cv2.imwrite(f"{debug_dir}/page_{page_num}_05_final.png", cleaned)
    
    return Image.fromarray(cleaned)

def try_multiple_ocr_configs(image):
    """
    Try different Tesseract configurations and return the best result
    """
    configs = [
        '--psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,!?";:-()[]{}/',  # Alphanumeric + common punctuation
        '--psm 6',  # Single uniform block
        '--psm 4',  # Single column of text
        '--psm 3',  # Fully automatic page segmentation
        '--psm 1',  # Automatic page segmentation with OSD
        '--psm 11', # Sparse text
        '--psm 13', # Raw line. Treat the image as a single text line
    ]
    
    best_text = ""
    best_confidence = 0
    best_config = ""
    
    for config in configs:
        try:
            # Get OCR result with confidence data
            data = pytesseract.image_to_data(
                image, 
                config=config, 
                output_type=pytesseract.Output.DICT
            )
            
            # Calculate average confidence (excluding -1 values)
            confidences = [int(x) for x in data['conf'] if int(x) > 0]
            if not confidences:
                continue
                
            avg_confidence = sum(confidences) / len(confidences)
            
            # Get the actual text
            text = pytesseract.image_to_string(image, config=config).strip()
            
            # Prefer results with higher confidence and more text
            score = avg_confidence * (1 + len(text) / 1000)  # Bonus for longer text
            
            if score > best_confidence and len(text) > 10:  # Minimum text length
                best_confidence = score
                best_text = text
                best_config = config
                
        except Exception as e:
            print(f"   Config failed: {config[:20]}... ({str(e)[:50]})")
            continue
    
    return best_text, best_confidence, best_config

def extract_text_from_pdf(pdf_path, output_base_dir="ocr_free_pdf", debug=False, dpi=300):
    """
    Main function to extract text from PDF using free Tesseract OCR
    
    Args:
        pdf_path: Path to the PDF file
        output_base_dir: Base directory to save results
        debug: If True, saves intermediate processing steps
        dpi: DPI for PDF to image conversion (higher = better quality, slower)
    """
    # Get PDF filename without extension for subfolder
    pdf_name = Path(pdf_path).stem
    output_dir = os.path.join(output_base_dir, pdf_name)
    
    print(f"🔍 Processing PDF: {pdf_path}")
    print(f"📁 Output directory: {output_dir}")
    
    # Create output directories
    os.makedirs(output_dir, exist_ok=True)
    if debug:
        debug_dir = os.path.join(output_dir, "debug_images")
        os.makedirs(debug_dir, exist_ok=True)
    else:
        debug_dir = None
    
    # Convert PDF to images
    print(f"📄 Converting PDF to images (DPI: {dpi})...")
    try:
        pages = convert_from_path(pdf_path, dpi=dpi, fmt='PNG')
        print(f"✅ Converted {len(pages)} pages")
    except Exception as e:
        print(f"❌ Error converting PDF: {e}")
        print("💡 Make sure you have poppler installed:")
        print("   macOS: brew install poppler")
        print("   Ubuntu: sudo apt-get install poppler-utils")
        return False
    
    # Process each page
    all_text = []
    total_confidence = 0
    
    for i, page in enumerate(pages, 1):
        print(f"\n🔄 Processing page {i}/{len(pages)}...")
        start_time = time.time()
        
        # Preprocess image
        processed_page = preprocess_image(page, debug_dir, i)
        
        # Extract text with multiple configurations
        text, confidence, config = try_multiple_ocr_configs(processed_page)
        
        # Store results
        page_header = f"{'='*50}\nPAGE {i}\n{'='*50}\n"
        page_text = page_header + text + "\n\n"
        all_text.append(page_text)
        total_confidence += confidence
        
        # Save individual page
        page_file = os.path.join(output_dir, f"page_{i:03d}.txt")
        with open(page_file, "w", encoding="utf-8") as f:
            f.write(text)
        
        # Progress info
        elapsed = time.time() - start_time
        print(f"✅ Page {i}: {len(text)} chars, confidence: {confidence:.1f}, time: {elapsed:.1f}s")
        print(f"   Best config: {config[:30]}...")
    
    # Save combined results
    combined_text = "\n".join(all_text)
    combined_file = os.path.join(output_dir, "complete_extracted_text.txt")
    
    with open(combined_file, "w", encoding="utf-8") as f:
        f.write(combined_text)
    
    # Summary
    avg_confidence = total_confidence / len(pages) if pages else 0
    total_chars = len(combined_text)
    
    print(f"\n🎉 EXTRACTION COMPLETE!")
    print(f"📊 Statistics:")
    print(f"   • Pages processed: {len(pages)}")
    print(f"   • Total characters: {total_chars:,}")
    print(f"   • Average confidence: {avg_confidence:.1f}%")
    print(f"   • Combined file: {combined_file}")
    print(f"   • Individual pages: {output_dir}/page_*.txt")
    
    if debug:
        print(f"   • Debug images: {debug_dir}/")
    
    return True

def process_multiple_pdfs(pdf_directory, output_base_dir="batch_ocr_free_pdf"):
    """
    Process all PDFs in a directory
    """
    pdf_files = list(Path(pdf_directory).glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in {pdf_directory}")
        return
    
    print(f"📚 Found {len(pdf_files)} PDF files")
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n{'='*60}")
        print(f"📖 Processing {i}/{len(pdf_files)}: {pdf_file.name}")
        print(f"{'='*60}")
        
        try:
            success = extract_text_from_pdf(str(pdf_file), output_base_dir)
            if success:
                print(f"✅ {pdf_file.name}: SUCCESS")
            else:
                print(f"❌ {pdf_file.name}: FAILED")
        except Exception as e:
            print(f"❌ {pdf_file.name}: ERROR - {e}")

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python packages
    try:
        import cv2
        print("✅ OpenCV: OK")
    except ImportError:
        print("❌ OpenCV: pip install opencv-python")
        return False
    
    try:
        import pytesseract
        print("✅ PyTesseract: OK")
    except ImportError:
        print("❌ PyTesseract: pip install pytesseract")
        return False
    
    try:
        from pdf2image import convert_from_path
        print("✅ PDF2Image: OK")
    except ImportError:
        print("❌ PDF2Image: pip install pdf2image")
        return False
    
    # Check Tesseract binary
    try:
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract: {version}")
    except Exception:
        print("❌ Tesseract binary not found")
        print("   Install: brew install tesseract (macOS) or sudo apt-get install tesseract-ocr (Ubuntu)")
        return False
    
    # Test poppler (via pdf2image)
    try:
        # This will fail if poppler is not installed
        from pdf2image.exceptions import PDFInfoNotInstalledError
        print("✅ Poppler: OK")
    except:
        print("❌ Poppler: brew install poppler (macOS) or sudo apt-get install poppler-utils (Ubuntu)")
        return False
    
    print("🎉 All dependencies are installed!")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Free OCR for PDF files using Tesseract")
    parser.add_argument("pdf_path", nargs="?", help="Path to PDF file or directory")
    parser.add_argument("--output", "-o", default="ocr_free_pdf", help="Output directory")
    parser.add_argument("--debug", action="store_true", help="Save debug images")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for image conversion (default: 300)")
    parser.add_argument("--batch", action="store_true", help="Process all PDFs in directory")
    parser.add_argument("--check", action="store_true", help="Check dependencies only")
    
    args = parser.parse_args()
    
    if args.check:
        check_dependencies()
    elif args.pdf_path:
        if args.batch:
            process_multiple_pdfs(args.pdf_path, args.output)
        else:
            if os.path.exists(args.pdf_path):
                extract_text_from_pdf(args.pdf_path, args.output, args.debug, args.dpi)
            else:
                print(f"❌ File not found: {args.pdf_path}")
    else:
        print("Free OCR Tool - Extract text from PDF files using Tesseract")
        print("\nUsage:")
        print("  python ocr_free.py document.pdf")
        print("  python ocr_free.py document.pdf --debug --dpi 600")
        print("  python ocr_free.py /path/to/pdfs/ --batch")
        print("  python ocr_free.py --check")
        print("\nOutput Structure:")
        print("  ocr_free_pdf/")
        print("    ├── document_name/")
        print("    │   ├── complete_extracted_text.txt")
        print("    │   ├── page_001.txt, page_002.txt, ...")
        print("    │   └── debug_images/ (if --debug)")
        print("\nOptions:")
        print("  --output DIR     Base output directory (default: ocr_free_pdf)")
        print("  --debug          Save intermediate processing images")
        print("  --dpi N          Image resolution (default: 300, try 600 for small text)")
        print("  --batch          Process all PDFs in directory")
        print("  --check          Check if dependencies are installed")
