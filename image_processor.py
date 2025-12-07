"""
Image processing module for loading, transforming, and preparing images.
"""

from PIL import Image, ImageDraw
from typing import Tuple
from models import ImageItem, CropRect
import io


class ImageProcessor:
    """Handles image loading and transformation."""
    
    @staticmethod
    def load_image(file_path: str) -> Image.Image:
        """Load an image from file."""
        try:
            img = Image.open(file_path)
            # Convert to RGB if needed (handles RGBA, grayscale, etc.)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            return img
        except Exception as e:
            raise ValueError(f"Failed to load image {file_path}: {str(e)}")
    
    @staticmethod
    def apply_crop(img: Image.Image, crop: CropRect) -> Image.Image:
        """Apply crop to image using normalized coordinates."""
        width, height = img.size
        
        # Convert normalized coordinates to pixels
        left = int(crop.x * width)
        top = int(crop.y * height)
        right = int((crop.x + crop.width) * width)
        bottom = int((crop.y + crop.height) * height)
        
        # Ensure coordinates are within bounds
        left = max(0, min(left, width))
        top = max(0, min(top, height))
        right = max(left, min(right, width))
        bottom = max(top, min(bottom, height))
        
        return img.crop((left, top, right, bottom))
    
    @staticmethod
    def rotate_image(img: Image.Image, angle: int) -> Image.Image:
        """Rotate image by angle (90, 180, 270 degrees)."""
        if angle % 360 == 0:
            return img
        # PIL rotates counter-clockwise, but we want clockwise
        return img.rotate(-angle, expand=True)
    
    @staticmethod
    def scale_to_fit(img: Image.Image, max_width: float, max_height: float, 
                     scale_factor: float = 1.0) -> Tuple[int, int]:
        """
        Calculate dimensions to fit image within max bounds while maintaining aspect ratio.
        
        Returns:
            Tuple of (width, height) in pixels
        """
        img_width, img_height = img.size
        aspect_ratio = img_width / img_height
        
        # Calculate dimensions that fit within bounds
        if img_width / max_width > img_height / max_height:
            # Width is the limiting factor
            new_width = max_width
            new_height = max_width / aspect_ratio
        else:
            # Height is the limiting factor
            new_height = max_height
            new_width = max_height * aspect_ratio
        
        # Apply additional scale factor
        new_width = int(new_width * scale_factor)
        new_height = int(new_height * scale_factor)
        
        return (new_width, new_height)
    
    @staticmethod
    def place_on_background(img: Image.Image, page_width: int, page_height: int,
                           bg_color: Tuple[int, int, int],
                           pos_x: float = 0.5, pos_y: float = 0.5) -> Image.Image:
        """
        Place image on a background of specified size.
        
        Args:
            img: Image to place
            page_width: Background width in pixels
            page_height: Background height in pixels
            bg_color: Background color (R, G, B)
            pos_x: Normalized X position (0-1, 0.5 = center)
            pos_y: Normalized Y position (0-1, 0.5 = center)
        
        Returns:
            New image with background
        """
        # Create background
        background = Image.new('RGB', (page_width, page_height), bg_color)
        
        # Calculate position to center the image
        img_width, img_height = img.size
        x = int((page_width - img_width) * pos_x)
        y = int((page_height - img_height) * pos_y)
        
        # Paste image onto background
        background.paste(img, (x, y))
        
        return background
    
    @staticmethod
    def process_image_item(item: ImageItem, page_width: float, page_height: float,
                          margin: float, bg_color: Tuple[int, int, int]) -> Image.Image:
        """
        Process an image item with all transformations applied.
        
        Args:
            item: ImageItem with transformation parameters
            page_width: Page width in points
            page_height: Page height in points
            margin: Margin in points
            bg_color: Background color
        
        Returns:
            Processed PIL Image ready for PDF
        """
        # Load image
        img = ImageProcessor.load_image(item.file_path)
        
        # Apply crop
        if not (item.crop.x == 0 and item.crop.y == 0 and 
                item.crop.width == 1.0 and item.crop.height == 1.0):
            img = ImageProcessor.apply_crop(img, item.crop)
        
        # Apply rotation
        if item.rotation != 0:
            img = ImageProcessor.rotate_image(img, item.rotation)
        
        # Calculate available space (page minus margins)
        available_width = page_width - 2 * margin
        available_height = page_height - 2 * margin
        
        # Calculate scaled dimensions
        if item.fit_to_page:
            new_size = ImageProcessor.scale_to_fit(img, available_width, 
                                                  available_height, item.scale)
        else:
            # Use original size with scale factor
            new_size = (int(img.width * item.scale), int(img.height * item.scale))
        
        # Resize image
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Place on background (convert page size to pixels for consistency)
        # For PDF, we'll use 72 DPI, so points = pixels
        result = ImageProcessor.place_on_background(
            img, 
            int(page_width), 
            int(page_height),
            bg_color,
            item.position_x,
            item.position_y
        )
        
        return result
