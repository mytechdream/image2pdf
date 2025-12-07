"""
Main window for the Image to PDF application.
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QSplitter,
                            QMenuBar, QMenu, QAction, QFileDialog, QMessageBox,
                            QToolBar, QStatusBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from models import ProjectState
from preview_widget import PreviewWidget
from control_panel import ControlPanel
from pdf_generator import PDFGenerator
from pdf_merge_dialog import PDFMergeDialog
import os


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.state = ProjectState()
        self.init_ui()
        self.update_preview()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Image to PDF Converter")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Create preview widget (left side)
        self.preview_widget = PreviewWidget()
        splitter.addWidget(self.preview_widget)
        
        # Create control panel (right side)
        self.control_panel = ControlPanel(self.state)
        self.control_panel.parameter_changed.connect(self.on_parameter_changed)
        self.control_panel.image_list_changed.connect(self.on_image_list_changed)
        splitter.addWidget(self.control_panel)
        
        # Create menu bar (after control panel is created)
        self.create_menu_bar()
        
        # Create toolbar (after control panel is created)
        self.create_toolbar()
        
        # Set initial sizes (70% preview, 30% control)
        splitter.setSizes([700, 300])
        
        # Add splitter to main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(splitter)
        main_layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(main_layout)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Apply stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
                min-height: 25px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
    
    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        # Add images action
        add_action = QAction("Add Images...", self)
        add_action.setShortcut("Ctrl+O")
        add_action.triggered.connect(self.control_panel.add_images)
        file_menu.addAction(add_action)
        
        file_menu.addSeparator()
        
        # Export PDF action
        export_action = QAction("Export to PDF...", self)
        export_action.setShortcut("Ctrl+S")
        export_action.triggered.connect(self.export_pdf)
        file_menu.addAction(export_action)
        
        # Merge PDFs action
        merge_action = QAction("Merge PDFs...", self)
        merge_action.setShortcut("Ctrl+M")
        merge_action.triggered.connect(self.show_merge_dialog)
        file_menu.addAction(merge_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Create the toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Add images button
        add_action = QAction("Add Images", self)
        add_action.triggered.connect(self.control_panel.add_images)
        toolbar.addAction(add_action)
        
        toolbar.addSeparator()
        
        # Export PDF button
        export_action = QAction("Export PDF", self)
        export_action.triggered.connect(self.export_pdf)
        toolbar.addAction(export_action)
        
        # Merge PDFs button
        merge_action = QAction("Merge PDFs", self)
        merge_action.triggered.connect(self.show_merge_dialog)
        toolbar.addAction(merge_action)
    
    def on_parameter_changed(self):
        """Handle parameter changes."""
        self.update_preview()
    
    def on_image_list_changed(self):
        """Handle image list changes."""
        self.update_preview()
        self.update_status()
    
    def update_preview(self):
        """Update the preview widget."""
        if not self.state.images:
            self.preview_widget.update_preview(None)
            return
        
        # Get the current image index
        current_index = self.state.current_image_index
        if current_index < 0 and len(self.state.images) > 0:
            current_index = 0
        
        if current_index >= len(self.state.images):
            current_index = len(self.state.images) - 1
        
        if current_index >= 0:
            try:
                # Generate preview for current page
                preview_image = PDFGenerator.generate_preview_image(
                    self.state.images,
                    self.state.page_config,
                    current_index
                )
                self.preview_widget.update_preview(preview_image)
                self.status_bar.showMessage(
                    f"Page {current_index + 1} of {len(self.state.images)}"
                )
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Preview Error",
                    f"Failed to generate preview: {str(e)}"
                )
                self.preview_widget.update_preview(None)
    
    def update_status(self):
        """Update the status bar."""
        if self.state.images:
            current = self.state.current_image_index + 1 if self.state.current_image_index >= 0 else 1
            total = len(self.state.images)
            self.status_bar.showMessage(f"Page {current} of {total}")
        else:
            self.status_bar.showMessage("No images loaded")
    
    def export_pdf(self):
        """Export images to PDF."""
        if not self.state.images:
            QMessageBox.warning(
                self,
                "No Images",
                "Please add images before exporting to PDF."
            )
            return
        
        # Open save dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF",
            "",
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            # Ensure .pdf extension
            if not file_path.lower().endswith('.pdf'):
                file_path += '.pdf'
            
            try:
                # Generate PDF
                success = PDFGenerator.generate_pdf(
                    file_path,
                    self.state.images,
                    self.state.page_config
                )
                
                if success:
                    QMessageBox.information(
                        self,
                        "Success",
                        f"PDF saved successfully to:\n{file_path}"
                    )
                    self.status_bar.showMessage(f"PDF exported to {os.path.basename(file_path)}")
                else:
                    QMessageBox.warning(
                        self,
                        "Export Failed",
                        "Failed to generate PDF. Please check your images and try again."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"An error occurred while exporting:\n{str(e)}"
                )
    
    def show_merge_dialog(self):
        """Show the PDF merge dialog."""
        dialog = PDFMergeDialog(self)
        dialog.exec_()
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Image to PDF Converter",
            "<h3>Image to PDF Converter</h3>"
            "<p>A desktop application for converting images to PDF files.</p>"
            "<p>Features:</p>"
            "<ul>"
            "<li>Support for multiple image formats</li>"
            "<li>Adjustable page sizes (A4, Letter, etc.)</li>"
            "<li>Image transformation (scale, rotate, position)</li>"
            "<li>Real-time PDF preview</li>"
            "<li>Merge multiple PDF files</li>"
            "</ul>"
            "<p>Version 1.0</p>"
        )
