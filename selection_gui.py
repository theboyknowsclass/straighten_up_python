from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QFileDialog


class SelectionGui(QVBoxLayout):
    def __init__(self, QWidget):
        super().__init__()
        self.parent = QWidget
        self.select_images_button = None
        self.images = {}
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.select_images_button = QPushButton('Select Images...', self.parent)
        self.select_images_button.setMaximumWidth(200)  # Set maximum width
        self.select_images_button.clicked.connect(self.openImageDialog)
        layout.addWidget(self.select_images_button)

    def openImageDialog(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_filter = "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
            file_names, _ = QFileDialog.getOpenFileNames(self.parent, "Select Images", "", file_filter, options=options)
            if file_names:
                print("Selected images:", file_names)
        except Exception as e:
            print("Error:", e)

    def closeEvent(self, event):
        event.accept()