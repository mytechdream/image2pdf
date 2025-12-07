"""
PDF Merge Dialog - UI for merging multiple PDF files.
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                            QListWidget, QLabel, QFileDialog, QMessageBox,
                            QProgressDialog, QGroupBox, QListWidgetItem)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from pdf_merger import PDFMerger
import os


class MergeWorker(QThread):
    """Worker thread for PDF merging to avoid blocking UI."""
    
    progress = pyqtSignal(int, int)  # current, total
    finished = pyqtSignal(bool, str)  # success, message
    
    def __init__(self, pdf_paths, output_path):
        super().__init__()
        self.pdf_paths = pdf_paths
        self.output_path = output_path
    
    def run(self):
        """Run the merge operation in background."""
        try:
            PDFMerger.merge_pdfs(
                self.pdf_paths,
                self.output_path,
                progress_callback=lambda curr, total: self.progress.emit(curr, total)
            )
            self.finished.emit(True, "PDF files merged successfully!")
        except Exception as e:
            self.finished.emit(False, f"Failed to merge PDFs: {str(e)}")


class PDFMergeDialog(QDialog):
    """Dialog for merging multiple PDF files."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pdf_list = []  # List of PDF file paths
        self.init_ui()
        self.setWindowTitle("Merge PDF Files")
        self.resize(600, 500)
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Instructions
        info_label = QLabel("Add PDF files to merge them into a single document:")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # PDF list group
        list_group = QGroupBox("PDF Files")
        list_layout = QVBoxLayout()
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self.on_selection_changed)
        list_layout.addWidget(self.list_widget)
        
        # List control buttons
        list_btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Add PDFs...")
        self.add_btn.clicked.connect(self.add_pdfs)
        list_btn_layout.addWidget(self.add_btn)
        
        self.remove_btn = QPushButton("Remove")
        self.remove_btn.clicked.connect(self.remove_selected)
        self.remove_btn.setEnabled(False)
        list_btn_layout.addWidget(self.remove_btn)
        
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.clear_all)
        self.clear_btn.setEnabled(False)
        list_btn_layout.addWidget(self.clear_btn)
        
        list_btn_layout.addStretch()
        
        self.move_up_btn = QPushButton("↑ Move Up")
        self.move_up_btn.clicked.connect(self.move_up)
        self.move_up_btn.setEnabled(False)
        list_btn_layout.addWidget(self.move_up_btn)
        
        self.move_down_btn = QPushButton("↓ Move Down")
        self.move_down_btn.clicked.connect(self.move_down)
        self.move_down_btn.setEnabled(False)
        list_btn_layout.addWidget(self.move_down_btn)
        
        list_layout.addLayout(list_btn_layout)
        
        # File info label
        self.info_label = QLabel("No files added")
        self.info_label.setStyleSheet("color: #666; font-style: italic;")
        list_layout.addWidget(self.info_label)
        
        list_group.setLayout(list_layout)
        layout.addWidget(list_group)
        
        # Dialog buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.merge_btn = QPushButton("Merge PDFs...")
        self.merge_btn.clicked.connect(self.merge_pdfs)
        self.merge_btn.setEnabled(False)
        self.merge_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        button_layout.addWidget(self.merge_btn)
        
        cancel_btn = QPushButton("Close")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def add_pdfs(self):
        """Open file dialog to add PDF files."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select PDF Files",
            "",
            "PDF Files (*.pdf)"
        )
        
        if files:
            for file_path in files:
                if file_path not in self.pdf_list:
                    # Get PDF info
                    info = PDFMerger.get_pdf_info(file_path)
                    
                    if "error" in info:
                        QMessageBox.warning(
                            self,
                            "Invalid PDF",
                            f"Cannot add '{os.path.basename(file_path)}':\n{info['error']}"
                        )
                        continue
                    
                    # Add to list
                    self.pdf_list.append(file_path)
                    
                    # Add to list widget with page count
                    filename = os.path.basename(file_path)
                    page_count = info.get('page_count', '?')
                    item_text = f"{filename} ({page_count} pages)"
                    self.list_widget.addItem(item_text)
            
            self.update_ui_state()
    
    def remove_selected(self):
        """Remove selected PDF from list."""
        current_row = self.list_widget.currentRow()
        if current_row >= 0:
            self.pdf_list.pop(current_row)
            self.list_widget.takeItem(current_row)
            self.update_ui_state()
    
    def clear_all(self):
        """Clear all PDFs from list."""
        reply = QMessageBox.question(
            self,
            "Clear All",
            "Remove all PDF files from the list?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.pdf_list.clear()
            self.list_widget.clear()
            self.update_ui_state()
    
    def move_up(self):
        """Move selected item up in the list."""
        current_row = self.list_widget.currentRow()
        if current_row > 0:
            # Swap in data list
            self.pdf_list[current_row], self.pdf_list[current_row - 1] = \
                self.pdf_list[current_row - 1], self.pdf_list[current_row]
            
            # Swap in UI
            item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row - 1, item)
            self.list_widget.setCurrentRow(current_row - 1)
    
    def move_down(self):
        """Move selected item down in the list."""
        current_row = self.list_widget.currentRow()
        if current_row < len(self.pdf_list) - 1:
            # Swap in data list
            self.pdf_list[current_row], self.pdf_list[current_row + 1] = \
                self.pdf_list[current_row + 1], self.pdf_list[current_row]
            
            # Swap in UI
            item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row + 1, item)
            self.list_widget.setCurrentRow(current_row + 1)
    
    def on_selection_changed(self, row):
        """Handle selection change in the list."""
        has_selection = row >= 0
        self.remove_btn.setEnabled(has_selection)
        self.move_up_btn.setEnabled(has_selection and row > 0)
        self.move_down_btn.setEnabled(has_selection and row < len(self.pdf_list) - 1)
    
    def update_ui_state(self):
        """Update UI based on current state."""
        has_files = len(self.pdf_list) > 0
        has_multiple = len(self.pdf_list) > 1
        
        self.clear_btn.setEnabled(has_files)
        self.merge_btn.setEnabled(has_multiple)
        
        if has_files:
            total_pages = 0
            for pdf_path in self.pdf_list:
                info = PDFMerger.get_pdf_info(pdf_path)
                total_pages += info.get('page_count', 0)
            
            self.info_label.setText(
                f"{len(self.pdf_list)} file(s) selected, {total_pages} total pages"
            )
        else:
            self.info_label.setText("No files added")
        
        # Update move button states
        current_row = self.list_widget.currentRow()
        self.on_selection_changed(current_row)
    
    def merge_pdfs(self):
        """Start the merge process."""
        if len(self.pdf_list) < 2:
            QMessageBox.warning(
                self,
                "Insufficient Files",
                "Please add at least 2 PDF files to merge."
            )
            return
        
        # Ask for output location
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Merged PDF",
            "merged.pdf",
            "PDF Files (*.pdf)"
        )
        
        if not output_path:
            return
        
        # Ensure .pdf extension
        if not output_path.lower().endswith('.pdf'):
            output_path += '.pdf'
        
        # Create progress dialog
        progress = QProgressDialog("Merging PDF files...", "Cancel", 0, len(self.pdf_list), self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setAutoClose(True)
        progress.setAutoReset(True)
        
        # Create and start worker thread
        self.worker = MergeWorker(self.pdf_list, output_path)
        self.worker.progress.connect(lambda curr, total: progress.setValue(curr))
        self.worker.finished.connect(lambda success, msg: self.on_merge_finished(success, msg, output_path))
        
        # Handle cancel
        progress.canceled.connect(self.worker.terminate)
        
        self.worker.start()
        progress.exec_()
    
    def on_merge_finished(self, success, message, output_path):
        """Handle merge completion."""
        if success:
            QMessageBox.information(
                self,
                "Success",
                f"{message}\n\nSaved to:\n{output_path}"
            )
            self.accept()  # Close dialog
        else:
            QMessageBox.critical(
                self,
                "Error",
                message
            )
