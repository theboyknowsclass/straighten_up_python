import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog

class StraightenUpApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Straighten Up')
        self.setGeometry(100, 100, 800, 600)  # Set initial size

        layout = QVBoxLayout()

        self.select_images_button = QPushButton('Select Images...', self)
        self.select_images_button.setMaximumWidth(200)  # Set maximum width
        self.select_images_button.clicked.connect(self.openImageDialog)
        layout.addWidget(self.select_images_button)

        self.setLayout(layout)
        self.show()

    def openImageDialog(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_filter = "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
            file_names, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", file_filter, options=options)
            if file_names:
                print("Selected images:", file_names)
        except Exception as e:
            print("Error:", e)

    def closeEvent(self, event):
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StraightenUpApp()
    sys.exit(app.exec_())
