import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QListWidgetItem

from image_viewer import ImageViewer


class ConfirmationGui(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.state.register_observer(self.update)

        vertical_layout = QVBoxLayout()

        # Create the QListWidget for displaying thumbnails
        self.list_widget = QListWidget()
        self.thumbnail_size = 100  # Define a square size for the thumbnails
        self.list_widget.setIconSize(QPixmap(self.thumbnail_size, self.thumbnail_size).size())
        self.list_widget.itemClicked.connect(self.show_full_image)

        horizontal_layout = QHBoxLayout()

        self.process_button = QPushButton('Process', self)
        self.process_button.setMinimumWidth(200)
        self.process_button.setMaximumWidth(250)
        self.process_button.clicked.connect(self.process_images)

        self.clear_button = QPushButton('Clear', self)
        self.clear_button.setMinimumWidth(200)
        self.clear_button.setMaximumWidth(250)
        self.clear_button.clicked.connect(self.clear_images)

        horizontal_layout.addStretch(1)
        horizontal_layout.addWidget(self.clear_button)
        horizontal_layout.addStretch(1)
        horizontal_layout.addWidget(self.process_button)
        horizontal_layout.addStretch(1)

        vertical_layout.addWidget(self.list_widget)
        vertical_layout.addLayout(horizontal_layout)

        self.setLayout(vertical_layout)

    def update(self, state):
        self.list_widget.clear()
        for image in state.images:
            # Load the original image
            pixmap = QPixmap(image)

            # Scale the image while preserving aspect ratio
            thumbnail = pixmap.scaled(self.thumbnail_size, self.thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Create an item with the scaled image and the file name
            item = QListWidgetItem(QIcon(thumbnail), os.path.basename(image))
            self.list_widget.addItem(item)

    def show_full_image(self, item):
        """Open a new window to display the full-sized image."""
        viewer = ImageViewer(item.text())
        viewer.exec_()

    def process_images(self):
        self.state.start_process()

    def clear_images(self):
        self.state.clear_input_images()


