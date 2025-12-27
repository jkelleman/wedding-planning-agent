"""
File organizer module for renaming and organizing wedding documents.
"""
import os
import shutil
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class FileOrganizer:
    """Organizes files with clear naming conventions."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.input_dir = Path(config['file_organization']['input_dir'])
        self.output_dir = Path(config['file_organization']['output_dir'])
        self.categories = config['file_organization']['categories']
        
        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        for category in self.categories:
            (self.output_dir / category).mkdir(exist_ok=True)
    
    def organize_file(self, scan_result: Dict) -> Dict[str, str]:
        """
        Organize a file based on its scan results.
        
        Returns:
            Dict with old_path, new_path, and status.
        """
        if "error" in scan_result:
            return {"status": "error", "message": scan_result["error"]}
        
        old_path = Path(scan_result["path"])
        metadata = scan_result["metadata"]
        
        # Determine category
        category = metadata.get("category", "other")
        if category not in self.categories:
            category = "other"
        
        # Build new filename
        parts = []
        
        # Add category prefix
        parts.append(category)
        
        # Add venue name if available
        if metadata.get("venue_name"):
            venue_clean = self._sanitize_filename(metadata["venue_name"])
            parts.append(venue_clean)
        
        # Add price if available
        if metadata.get("price"):
            parts.append(f"${int(metadata['price'])}")
        
        # Add original filename (without extension)
        parts.append(old_path.stem)
        
        # Combine and add extension
        new_filename = "_".join(parts) + old_path.suffix
        new_path = self.output_dir / category / new_filename
        
        # Copy file to organized location
        try:
            shutil.copy2(old_path, new_path)
            return {
                "status": "success",
                "old_path": str(old_path),
                "new_path": str(new_path),
                "category": category
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to organize file: {e}",
                "old_path": str(old_path)
            }
    
    def organize_directory(self, directory: str = None) -> List[Dict]:
        """Organize all files in the input directory."""
        if directory is None:
            directory = self.input_dir
        else:
            directory = Path(directory)
        
        if not directory.exists():
            return [{"status": "error", "message": f"Directory not found: {directory}"}]
        
        results = []
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.png', '.jpg', '.jpeg']:
                # Import here to avoid circular dependency
                from .scanner import DocumentScanner
                scanner = DocumentScanner()
                scan_result = scanner.scan_file(str(file_path))
                organize_result = self.organize_file(scan_result)
                organize_result["scan_metadata"] = scan_result.get("metadata", {})
                results.append(organize_result)
        
        return results
    
    def _sanitize_filename(self, name: str) -> str:
        """Remove invalid characters from filename."""
        # Replace invalid characters with underscore
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        # Remove multiple consecutive underscores
        while '__' in name:
            name = name.replace('__', '_')
        return name.strip('_')
