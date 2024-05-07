from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QDialog


class ImageViewer(QDialog):
    def __init__(self, file_path):
        super().__init__()

        # Set up the dialog properties
        self.setWindowTitle('Full Image Viewer')
        self.setGeometry(100, 100, 800, 600)

        # Create a QLabel to show the full image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        # Load the full-sized image and display it on the label
        full_image = QPixmap(file_path)
        self.image_label.setPixmap(full_image)

        # Add the QLabel to a scrollable area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.image_label)

        # Add the scroll area to the layout
        layout = QVBoxLayout()
        layout.addWidget(scroll_area)

        # Set the dialog layout
        self.setLayout(layout)