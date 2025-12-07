"""
PDF merger module using PyMuPDF (fitz).
"""

import fitz  # PyMuPDF
from typing import List, Optional, Callable
import os


class PDFMerger:
    """Handles PDF merging operations."""
    
    @staticmethod
    def merge_pdfs(pdf_paths: List[str], output_path: str, 
                   progress_callback: Optional[Callable[[int, int], None]] = None) -> bool:
        """
        Merge multiple PDF files into a single PDF.
        
        Args:
            pdf_paths: List of paths to PDF files to merge
            output_path: Path where the merged PDF will be saved
            progress_callback: Optional callback function(current, total) for progress updates
        
        Returns:
            True if successful, False otherwise
        
        Raises:
            ValueError: If pdf_paths is empty or contains invalid paths
            Exception: If merge operation fails
        """
        if not pdf_paths:
            raise ValueError("No PDF files provided for merging")
        
        # Validate all input files exist
        for path in pdf_paths:
            if not os.path.exists(path):
                raise ValueError(f"File not found: {path}")
            if not path.lower().endswith('.pdf'):
                raise ValueError(f"Not a PDF file: {path}")
        
        try:
            # Create a new PDF document for the merged result
            merged_pdf = fitz.open()
            
            total_files = len(pdf_paths)
            
            # Process each PDF file
            for index, pdf_path in enumerate(pdf_paths):
                try:
                    # Open the PDF
                    pdf_doc = fitz.open(pdf_path)
                    
                    # Insert all pages from this PDF into the merged PDF
                    merged_pdf.insert_pdf(pdf_doc)
                    
                    # Close the source PDF
                    pdf_doc.close()
                    
                    # Report progress
                    if progress_callback:
                        progress_callback(index + 1, total_files)
                        
                except Exception as e:
                    # Close resources and re-raise with context
                    merged_pdf.close()
                    raise Exception(f"Error processing '{os.path.basename(pdf_path)}': {str(e)}")
            
            # Save the merged PDF
            merged_pdf.save(output_path)
            merged_pdf.close()
            
            return True
            
        except Exception as e:
            print(f"Error merging PDFs: {str(e)}")
            raise
    
    @staticmethod
    def get_pdf_info(pdf_path: str) -> dict:
        """
        Get information about a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
        
        Returns:
            Dictionary containing PDF metadata (pages, title, author, etc.)
        """
        try:
            if not os.path.exists(pdf_path):
                return {"error": "File not found"}
            
            pdf_doc = fitz.open(pdf_path)
            
            info = {
                "page_count": len(pdf_doc),
                "filename": os.path.basename(pdf_path),
                "file_size": os.path.getsize(pdf_path),
                "metadata": pdf_doc.metadata
            }
            
            pdf_doc.close()
            return info
            
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_first_page_thumbnail(pdf_path: str, max_size: tuple = (200, 200)):
        """
        Generate a thumbnail of the first page of a PDF.
        
        Args:
            pdf_path: Path to the PDF file
            max_size: Maximum size for the thumbnail (width, height)
        
        Returns:
            PIL Image object or None if failed
        """
        try:
            from PIL import Image
            import io
            
            pdf_doc = fitz.open(pdf_path)
            
            if len(pdf_doc) == 0:
                pdf_doc.close()
                return None
            
            # Get the first page
            page = pdf_doc[0]
            
            # Render page to an image
            # Calculate zoom to fit max_size
            page_rect = page.rect
            zoom_x = max_size[0] / page_rect.width
            zoom_y = max_size[1] / page_rect.height
            zoom = min(zoom_x, zoom_y)
            
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            pdf_doc.close()
            return img
            
        except Exception as e:
            print(f"Error generating thumbnail: {str(e)}")
            return None
