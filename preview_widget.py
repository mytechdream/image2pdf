"""
Preview widget for displaying PDF pages.
"""

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image
from typing import Optional


class PreviewWidget(QWidget):
    """Widget for displaying PDF preview."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_image = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scroll area for the preview
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setAlignment(Qt.AlignCenter)
        
        # Create label for displaying the image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #2b2b2b; padding: 20px;")
        self.image_label.setText("No preview available\n\nLoad images to see preview")
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #2b2b2b;
                color: #888888;
                padding: 20px;
                font-size: 14px;
            }
        """)
        
        scroll.setWidget(self.image_label)
        layout.addWidget(scroll)
    
    def update_preview(self, pil_image: Optional[Image.Image]):
        """
        Update the preview with a new PIL Image.
        
        Args:
            pil_image: PIL Image to display, or None to clear
        """
        if pil_image is None:
            self.image_label.clear()
            self.image_label.setText("No preview available\n\nLoad images to see preview")
            self.current_image = None
            return
        
        self.current_image = pil_image
        
        # Convert PIL Image to QPixmap
        # First convert to bytes
        img_rgb = pil_image.convert('RGB')
        data = img_rgb.tobytes('raw', 'RGB')
        
        # Create QImage
        qimage = QImage(data, img_rgb.width, img_rgb.height, 
                       img_rgb.width * 3, QImage.Format_RGB888)
        
        # Convert to QPixmap and scale to fit widget while maintaining aspect ratio
        pixmap = QPixmap.fromImage(qimage)
        
        # Scale pixmap to fit in the widget (max 800px width for good visibility)
        max_width = min(800, self.width() - 40)
        if pixmap.width() > max_width:
            pixmap = pixmap.scaledToWidth(max_width, Qt.SmoothTransformation)
        
        self.image_label.setPixmap(pixmap)
