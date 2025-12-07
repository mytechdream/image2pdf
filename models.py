"""
Data models for the application.
"""

from dataclasses import dataclass, field
from typing import Tuple, Optional
from PyQt5.QtGui import QColor


@dataclass
class CropRect:
    """Rectangle for cropping, in normalized coordinates (0-1)."""
    x: float = 0.0
    y: float = 0.0
    width: float = 1.0
    height: float = 1.0


@dataclass
class ImageItem:
    """Represents an image with its transformation parameters."""
    file_path: str
    scale: float = 1.0  # Scale factor (1.0 = fit to page)
    position_x: float = 0.5  # Normalized X position (0-1, 0.5 = center)
    position_y: float = 0.5  # Normalized Y position (0-1, 0.5 = center)
    rotation: int = 0  # Rotation in degrees (0, 90, 180, 270)
    crop: CropRect = field(default_factory=CropRect)
    fit_to_page: bool = True  # If True, scale to fit page while maintaining aspect ratio


@dataclass
class PageConfig:
    """Page configuration settings."""
    format_name: str = 'A4'
    background_color: Tuple[int, int, int] = (255, 255, 255)  # RGB
    margin: float = 36.0  # Margin in points (0.5 inch)


@dataclass
class ProjectState:
    """Application state."""
    images: list = field(default_factory=list)  # List of ImageItem
    page_config: PageConfig = field(default_factory=PageConfig)
    current_image_index: int = -1  # Currently selected image
