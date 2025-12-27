"""
Document scanner module for extracting text from PDFs and images.
"""
import os
from pathlib import Path
from typing import Dict, Optional
import re

try:
    import pytesseract
    from PIL import Image
except ImportError:
    pytesseract = None
    Image = None

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None


class DocumentScanner:
    """Scans PDFs and PNGs to extract reception details."""
    
    def __init__(self):
        if pytesseract is None:
            print("Warning: pytesseract not installed. Image scanning disabled.")
        if PdfReader is None:
            print("Warning: PyPDF2 not installed. PDF scanning disabled.")
    
    def scan_file(self, file_path: str) -> Dict[str, any]:
        """
        Scan a file and extract key information.
        
        Returns:
            Dict with extracted text, venue name, price, date, category, etc.
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {"error": f"File not found: {file_path}"}
        
        result = {
            "filename": file_path.name,
            "path": str(file_path),
            "type": file_path.suffix.lower(),
            "text": "",
            "metadata": {}
        }
        
        # Extract text based on file type
        if file_path.suffix.lower() == '.pdf':
            result["text"] = self._scan_pdf(file_path)
        elif file_path.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            result["text"] = self._scan_image(file_path)
        else:
            result["error"] = f"Unsupported file type: {file_path.suffix}"
            return result
        
        # Extract metadata from text
        result["metadata"] = self._extract_metadata(result["text"])
        
        return result
    
    def _scan_pdf(self, file_path: Path) -> str:
        """Extract text from PDF."""
        if PdfReader is None:
            return "[PDF scanning unavailable - install PyPDF2]"
        
        try:
            reader = PdfReader(str(file_path))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            return f"[Error scanning PDF: {e}]"
    
    def _scan_image(self, file_path: Path) -> str:
        """Extract text from image using OCR."""
        if pytesseract is None or Image is None:
            return "[Image scanning unavailable - install pytesseract and Pillow]"
        
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            return f"[Error scanning image: {e}]"
    
    def _extract_metadata(self, text: str) -> Dict[str, any]:
        """Extract structured metadata from text."""
        metadata = {
            "venue_name": None,
            "price": None,
            "date": None,
            "category": None,
            "capacity": None,
            "dietary_options": []
        }
        
        # Extract price (e.g., $5,000, $50.00, 5000 USD)
        price_pattern = r'\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:USD|dollars?)?'
        prices = re.findall(price_pattern, text, re.IGNORECASE)
        if prices:
            # Take the largest number as likely the total price
            metadata["price"] = max([float(p.replace(',', '')) for p in prices])
        
        # Extract capacity/guest count
        capacity_pattern = r'(?:capacity|seats?|guests?)[\s:]*(\d+)'
        capacity_match = re.search(capacity_pattern, text, re.IGNORECASE)
        if capacity_match:
            metadata["capacity"] = int(capacity_match.group(1))
        
        # Detect category from keywords
        text_lower = text.lower()
        if any(word in text_lower for word in ['venue', 'location', 'hall', 'ballroom']):
            metadata["category"] = "venue"
        elif any(word in text_lower for word in ['catering', 'menu', 'food', 'dinner']):
            metadata["category"] = "catering"
        elif any(word in text_lower for word in ['floral', 'flowers', 'bouquet', 'arrangement']):
            metadata["category"] = "floral"
        elif any(word in text_lower for word in ['photo', 'photography', 'photographer']):
            metadata["category"] = "photography"
        elif any(word in text_lower for word in ['music', 'dj', 'band', 'entertainment']):
            metadata["category"] = "entertainment"
        
        # Extract dietary options
        dietary_keywords = ['vegetarian', 'vegan', 'gluten-free', 'dairy-free', 'kosher', 'halal']
        for keyword in dietary_keywords:
            if keyword in text_lower:
                metadata["dietary_options"].append(keyword)
        
        # Try to extract venue name (first capitalized phrase in first 200 chars)
        first_part = text[:200]
        venue_pattern = r'^([A-Z][A-Za-z\s&]+(?:Hall|Center|Venue|Gardens?|Estate|Manor|Club|Hotel))'
        venue_match = re.search(venue_pattern, first_part, re.MULTILINE)
        if venue_match:
            metadata["venue_name"] = venue_match.group(1).strip()
        
        return metadata
