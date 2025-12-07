"""
Control panel for adjusting image and page parameters.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                            QLabel, QComboBox, QPushButton, QListWidget,
                            QSlider, QSpinBox, QDoubleSpinBox, QCheckBox,
                            QColorDialog, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from models import ImageItem, PageConfig, ProjectState
from page_formats import PAGE_FORMATS
import os


class ControlPanel(QWidget):
    """Control panel for parameter adjustment."""
    
    # Signals
    parameter_changed = pyqtSignal()  # Emitted when any parameter changes
    image_list_changed = pyqtSignal()  # Emitted when image list changes
    
    def __init__(self, state: ProjectState, parent=None):
        super().__init__(parent)
        self.state = state
        self.updating_ui = False  # Flag to prevent recursive updates
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Page settings group
        page_group = QGroupBox("Page Settings")
        page_layout = QVBoxLayout()
        
        # Page format selector
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Page Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(PAGE_FORMATS.keys())
        self.format_combo.setCurrentText(self.state.page_config.format_name)
        self.format_combo.currentTextChanged.connect(self.on_format_changed)
        format_layout.addWidget(self.format_combo)
        page_layout.addLayout(format_layout)
        
        # Background color button
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Background:"))
        self.color_button = QPushButton()
        self.update_color_button()
        self.color_button.clicked.connect(self.choose_background_color)
        color_layout.addWidget(self.color_button)
        page_layout.addLayout(color_layout)
        
        # Margin control
        margin_layout = QHBoxLayout()
        margin_layout.addWidget(QLabel("Margin (pts):"))
        self.margin_spin = QDoubleSpinBox()
        self.margin_spin.setRange(0, 100)
        self.margin_spin.setValue(self.state.page_config.margin)
        self.margin_spin.setSingleStep(5)
        self.margin_spin.valueChanged.connect(self.on_margin_changed)
        margin_layout.addWidget(self.margin_spin)
        page_layout.addLayout(margin_layout)
        
        page_group.setLayout(page_layout)
        layout.addWidget(page_group)
        
        # Image list group
        list_group = QGroupBox("Images")
        list_layout = QVBoxLayout()
        
        # Image list widget
        self.image_list = QListWidget()
        self.image_list.currentRowChanged.connect(self.on_image_selected)
        list_layout.addWidget(self.image_list)
        
        # Buttons for image list management
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Add Images")
        self.add_btn.clicked.connect(self.add_images)
        btn_layout.addWidget(self.add_btn)
        
        self.remove_btn = QPushButton("Remove")
        self.remove_btn.clicked.connect(self.remove_current_image)
        self.remove_btn.setEnabled(False)
        btn_layout.addWidget(self.remove_btn)
        
        self.move_up_btn = QPushButton("↑")
        self.move_up_btn.clicked.connect(self.move_image_up)
        self.move_up_btn.setEnabled(False)
        btn_layout.addWidget(self.move_up_btn)
        
        self.move_down_btn = QPushButton("↓")
        self.move_down_btn.clicked.connect(self.move_image_down)
        self.move_down_btn.setEnabled(False)
        btn_layout.addWidget(self.move_down_btn)
        
        list_layout.addLayout(btn_layout)
        list_group.setLayout(list_layout)
        layout.addWidget(list_group)
        
        # Image transformation group
        self.transform_group = QGroupBox("Image Adjustments")
        self.transform_group.setEnabled(False)
        transform_layout = QVBoxLayout()
        
        # Fit to page checkbox
        self.fit_checkbox = QCheckBox("Fit to page")
        self.fit_checkbox.setChecked(True)
        self.fit_checkbox.stateChanged.connect(self.on_fit_changed)
        transform_layout.addWidget(self.fit_checkbox)
        
        # Scale slider
        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel("Scale:"))
        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setRange(10, 200)
        self.scale_slider.setValue(100)
        self.scale_slider.setTickPosition(QSlider.TicksBelow)
        self.scale_slider.setTickInterval(10)
        self.scale_slider.valueChanged.connect(self.on_scale_changed)
        scale_layout.addWidget(self.scale_slider)
        self.scale_label = QLabel("100%")
        scale_layout.addWidget(self.scale_label)
        transform_layout.addLayout(scale_layout)
        
        # Position controls
        pos_layout = QVBoxLayout()
        
        # X position
        x_layout = QHBoxLayout()
        x_layout.addWidget(QLabel("Position X:"))
        self.pos_x_slider = QSlider(Qt.Horizontal)
        self.pos_x_slider.setRange(0, 100)
        self.pos_x_slider.setValue(50)
        self.pos_x_slider.valueChanged.connect(self.on_position_changed)
        x_layout.addWidget(self.pos_x_slider)
        self.pos_x_label = QLabel("50%")
        x_layout.addWidget(self.pos_x_label)
        pos_layout.addLayout(x_layout)
        
        # Y position
        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel("Position Y:"))
        self.pos_y_slider = QSlider(Qt.Horizontal)
        self.pos_y_slider.setRange(0, 100)
        self.pos_y_slider.setValue(50)
        self.pos_y_slider.valueChanged.connect(self.on_position_changed)
        y_layout.addWidget(self.pos_y_slider)
        self.pos_y_label = QLabel("50%")
        y_layout.addWidget(self.pos_y_label)
        pos_layout.addLayout(y_layout)
        
        transform_layout.addLayout(pos_layout)
        
        # Rotation
        rotation_layout = QHBoxLayout()
        rotation_layout.addWidget(QLabel("Rotation:"))
        self.rotation_combo = QComboBox()
        self.rotation_combo.addItems(["0°", "90°", "180°", "270°"])
        self.rotation_combo.currentIndexChanged.connect(self.on_rotation_changed)
        rotation_layout.addWidget(self.rotation_combo)
        transform_layout.addLayout(rotation_layout)
        
        self.transform_group.setLayout(transform_layout)
        layout.addWidget(self.transform_group)
        
        layout.addStretch()
    
    def update_color_button(self):
        """Update the color button appearance."""
        r, g, b = self.state.page_config.background_color
        self.color_button.setStyleSheet(
            f"background-color: rgb({r}, {g}, {b}); min-height: 30px;"
        )
        self.color_button.setText(f"RGB({r}, {g}, {b})")
    
    def choose_background_color(self):
        """Open color picker dialog."""
        r, g, b = self.state.page_config.background_color
        initial_color = QColor(r, g, b)
        color = QColorDialog.getColor(initial_color, self, "Choose Background Color")
        
        if color.isValid():
            self.state.page_config.background_color = (color.red(), color.green(), color.blue())
            self.update_color_button()
            self.parameter_changed.emit()
    
    def on_format_changed(self, format_name: str):
        """Handle page format change."""
        if not self.updating_ui:
            self.state.page_config.format_name = format_name
            self.parameter_changed.emit()
    
    def on_margin_changed(self, value: float):
        """Handle margin change."""
        if not self.updating_ui:
            self.state.page_config.margin = value
            self.parameter_changed.emit()
    
    def add_images(self):
        """Open file dialog to add images."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp)"
        )
        
        if files:
            for file_path in files:
                item = ImageItem(file_path=file_path)
                self.state.images.append(item)
                # Add to list widget
                self.image_list.addItem(os.path.basename(file_path))
            
            # Select the first newly added image
            if len(self.state.images) > 0:
                self.image_list.setCurrentRow(len(self.state.images) - len(files))
            
            self.image_list_changed.emit()
    
    def remove_current_image(self):
        """Remove the currently selected image."""
        current_row = self.image_list.currentRow()
        if current_row >= 0:
            self.state.images.pop(current_row)
            self.image_list.takeItem(current_row)
            
            # Update selection
            if len(self.state.images) > 0:
                new_row = min(current_row, len(self.state.images) - 1)
                self.image_list.setCurrentRow(new_row)
                self.state.current_image_index = new_row
            else:
                self.state.current_image_index = -1
                self.transform_group.setEnabled(False)
            
            self.image_list_changed.emit()
    
    def move_image_up(self):
        """Move current image up in the list."""
        current_row = self.image_list.currentRow()
        if current_row > 0:
            # Swap in data
            self.state.images[current_row], self.state.images[current_row - 1] = \
                self.state.images[current_row - 1], self.state.images[current_row]
            
            # Swap in UI
            item = self.image_list.takeItem(current_row)
            self.image_list.insertItem(current_row - 1, item)
            self.image_list.setCurrentRow(current_row - 1)
            
            self.image_list_changed.emit()
    
    def move_image_down(self):
        """Move current image down in the list."""
        current_row = self.image_list.currentRow()
        if current_row < len(self.state.images) - 1:
            # Swap in data
            self.state.images[current_row], self.state.images[current_row + 1] = \
                self.state.images[current_row + 1], self.state.images[current_row]
            
            # Swap in UI
            item = self.image_list.takeItem(current_row)
            self.image_list.insertItem(current_row + 1, item)
            self.image_list.setCurrentRow(current_row + 1)
            
            self.image_list_changed.emit()
    
    def on_image_selected(self, row: int):
        """Handle image selection change."""
        if row >= 0 and row < len(self.state.images):
            self.state.current_image_index = row
            self.transform_group.setEnabled(True)
            self.remove_btn.setEnabled(True)
            self.move_up_btn.setEnabled(row > 0)
            self.move_down_btn.setEnabled(row < len(self.state.images) - 1)
            
            # Update controls with current image settings
            self.load_current_image_settings()
            self.parameter_changed.emit()
        else:
            self.state.current_image_index = -1
            self.transform_group.setEnabled(False)
            self.remove_btn.setEnabled(False)
            self.move_up_btn.setEnabled(False)
            self.move_down_btn.setEnabled(False)
    
    def load_current_image_settings(self):
        """Load current image settings into UI controls."""
        if self.state.current_image_index < 0:
            return
        
        self.updating_ui = True
        item = self.state.images[self.state.current_image_index]
        
        self.fit_checkbox.setChecked(item.fit_to_page)
        self.scale_slider.setValue(int(item.scale * 100))
        self.pos_x_slider.setValue(int(item.position_x * 100))
        self.pos_y_slider.setValue(int(item.position_y * 100))
        
        rotation_index = item.rotation // 90
        self.rotation_combo.setCurrentIndex(rotation_index)
        
        self.updating_ui = False
    
    def on_fit_changed(self, state):
        """Handle fit to page checkbox change."""
        if not self.updating_ui and self.state.current_image_index >= 0:
            item = self.state.images[self.state.current_image_index]
            item.fit_to_page = self.fit_checkbox.isChecked()
            self.parameter_changed.emit()
    
    def on_scale_changed(self, value: int):
        """Handle scale slider change."""
        scale = value / 100.0
        self.scale_label.setText(f"{value}%")
        
        if not self.updating_ui and self.state.current_image_index >= 0:
            item = self.state.images[self.state.current_image_index]
            item.scale = scale
            self.parameter_changed.emit()
    
    def on_position_changed(self):
        """Handle position slider changes."""
        pos_x = self.pos_x_slider.value() / 100.0
        pos_y = self.pos_y_slider.value() / 100.0
        
        self.pos_x_label.setText(f"{int(pos_x * 100)}%")
        self.pos_y_label.setText(f"{int(pos_y * 100)}%")
        
        if not self.updating_ui and self.state.current_image_index >= 0:
            item = self.state.images[self.state.current_image_index]
            item.position_x = pos_x
            item.position_y = pos_y
            self.parameter_changed.emit()
    
    def on_rotation_changed(self, index: int):
        """Handle rotation change."""
        if not self.updating_ui and self.state.current_image_index >= 0:
            item = self.state.images[self.state.current_image_index]
            item.rotation = index * 90
            self.parameter_changed.emit()
