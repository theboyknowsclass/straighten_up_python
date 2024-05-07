from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QFileDialog, QHBoxLayout, QWidget


class SelectionGui(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.select_images_button = None
        self.select_images_button = QPushButton('Select Images...')
        self.select_images_button.setMinimumWidth(200)
        self.select_images_button.setMaximumWidth(250)
        self.select_images_button.clicked.connect(self.open_image_dialog)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addStretch(1)
        horizontal_layout.addWidget(self.select_images_button)
        horizontal_layout.addStretch(1)

        vertical_layout = QVBoxLayout()
        vertical_layout.addStretch(1)
        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.addStretch(1)

        self.setLayout(vertical_layout)

    def open_image_dialog(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_filter = "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
            file_names, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", file_filter, options=options)
            if file_names:
                self.state.add_input_images(file_names)
        except Exception as e:
            print("Error:", e)
