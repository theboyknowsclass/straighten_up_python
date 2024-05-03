import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog

from selection_gui import SelectionGui


class StraightenUpApp(QWidget):
    def __init__(self):
        super().__init__()
        self.images = {}
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Straighten Up')
        self.setGeometry(100, 100, 800, 600)  # Set initial size

        self.setLayout(SelectionGui(self))
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StraightenUpApp()
    sys.exit(app.exec_())
