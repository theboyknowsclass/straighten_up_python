import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, \
    QHBoxLayout, QScrollArea, QSizePolicy
from PyQt5.QtGui import QPixmap

class StraightenUpApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Straighten Up")
        self.setGeometry(100, 100, 800, 600)  # (x, y, width, height)

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Add button to open file dialog
        self.open_button = QPushButton("Open Image(s)")
        self.open_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.open_button)

        # Scroll area for thumbnails
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Widget to contain thumbnails
        self.thumbnail_widget = QWidget()
        self.thumbnail_widget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        self.thumbnail_layout = QHBoxLayout(self.thumbnail_widget)
        self.scroll_area.setWidget(self.thumbnail_widget)

        # Add process button (initially disabled)
        self.process_button = QPushButton("Process")
        self.process_button.clicked.connect(self.process_files)
        self.process_button.setEnabled(False)
        self.layout.addWidget(self.process_button)

        self.show()

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Select Image(s)", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if files:
            print("Selected Files:", files)
            self.show_thumbnails(files)
            self.process_button.setEnabled(True)
        else:
            self.process_button.setEnabled(False)

    def show_thumbnails(self, image_files):
        for file in image_files:
            pixmap = QPixmap(file)
            scaled_pixmap = pixmap.scaledToWidth(100)  # Scale pixmap to width 100, maintaining aspect ratio
            label = QLabel()
            label.setPixmap(scaled_pixmap)
            self.thumbnail_layout.addWidget(label)

    def process_files(self):
        print("Processing files...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StraightenUpApp()
    sys.exit(app.exec_())
