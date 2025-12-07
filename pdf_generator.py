"""
PDF generation module using reportlab.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import io
from typing import List
from models import ImageItem, PageConfig
from page_formats import get_page_size
from image_processor import ImageProcessor


class PDFGenerator:
    """Handles PDF generation from processed images."""
    
    @staticmethod
    def generate_pdf(output_path: str, images: List[ImageItem], 
                    page_config: PageConfig) -> bool:
        """
        Generate PDF from list of image items.
        
        Args:
            output_path: Path to save PDF
            images: List of ImageItem objects
            page_config: Page configuration
        
        Returns:
            True if successful, False otherwise
        """
        if not images:
            return False
        
        try:
            # Get page size
            page_size = get_page_size(page_config.format_name)
            
            # Create PDF canvas
            c = canvas.Canvas(output_path, pagesize=(page_size.width, page_size.height))
            
            # Process each image
            for item in images:
                # Process image with transformations
                processed_img = ImageProcessor.process_image_item(
                    item,
                    page_size.width,
                    page_size.height,
                    page_config.margin,
                    page_config.background_color
                )
                
                # Convert PIL Image to bytes for reportlab
                img_buffer = io.BytesIO()
                processed_img.save(img_buffer, format='PNG')
                img_buffer.seek(0)
                
                # Draw image on PDF
                # Image already includes background and positioning
                c.drawImage(ImageReader(img_buffer), 
                          0, 0, 
                          width=page_size.width, 
                          height=page_size.height)
                
                # Add new page for next image (except for last one)
                if item != images[-1]:
                    c.showPage()
            
            # Save PDF
            c.save()
            return True
            
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return False
    
    @staticmethod
    def generate_preview_image(images: List[ImageItem], page_config: PageConfig,
                              page_index: int = 0) -> Image.Image:
        """
        Generate a preview image for a specific page.
        
        Args:
            images: List of ImageItem objects
            page_config: Page configuration
            page_index: Index of the page to preview (0-based)
        
        Returns:
            PIL Image of the page preview
        """
        if not images or page_index >= len(images):
            # Return empty page
            page_size = get_page_size(page_config.format_name)
            return Image.new('RGB', 
                           (int(page_size.width), int(page_size.height)), 
                           page_config.background_color)
        
        # Get the image item for this page
        item = images[page_index]
        page_size = get_page_size(page_config.format_name)
        
        # Process and return the image
        return ImageProcessor.process_image_item(
            item,
            page_size.width,
            page_size.height,
            page_config.margin,
            page_config.background_color
        )
