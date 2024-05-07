import sys
from PyQt5.QtWidgets import QApplication, QWidget, QStackedLayout

from confirmation_gui import ConfirmationGui
from process_gui import ProcessGui
from selection_gui import SelectionGui
from main_window_state import MainWindowState


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.state = MainWindowState()
        self.state.register_observer(self.update)
        self.setWindowTitle('Straighten Up')
        self.setGeometry(100, 100, 800, 600)  # Set initial size

        # add pages
        self.selection_gui = SelectionGui(self.state)
        self.confirmation_gui = ConfirmationGui(self.state)
        self.process_gui = ProcessGui(self.state)

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.selection_gui)
        self.stacked_layout.addWidget(self.confirmation_gui)
        self.stacked_layout.addWidget(self.process_gui)

        self.setLayout(self.stacked_layout)

    def update(self, state):
        self.stacked_layout.setCurrentIndex(state.gui_index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
