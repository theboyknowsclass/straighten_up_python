import os

import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSpinBox, QGroupBox, QLabel

from process_gui_state import ProcessGuiState, TransformParams
from transform import find_and_correct_perspective


def convert_cv_qt(label, cv_img):
    """Convert from an opencv image to QPixmap"""
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(convert_to_qt_format).scaled(label.width(), label.height(), Qt.KeepAspectRatio,
                                                          Qt.SmoothTransformation)


def get_new_filename(filename, directory="."):
    """
    Generate a new filename by adding '_corrected' before the extension.
    If a file with that name exists, a number is appended and incremented.

    Parameters:
    - filename (str): Original filename to base the new name on.
    - directory (str): Directory to check for existing files. Defaults to the current directory.

    Returns:
    - str: A new, unique filename in the specified directory.
    """
    # Get the base name and extension
    base, ext = os.path.splitext(filename)
    new_base = f"{base}_corrected"
    new_filename = f"{new_base}{ext}"

    # Initialize the counter for appending numbers
    counter = 1

    # Check if the new filename already exists in the directory
    while os.path.exists(os.path.join(directory, new_filename)):
        # Update new filename by appending/incrementing the number
        new_filename = f"{new_base}_{counter}{ext}"
        counter += 1

    return new_filename


class ProcessGui(QWidget):
    def __init__(self, state):
        super().__init__()
        # ProcessGuiState
        self.state = None
        # Main State
        self.images = None
        self.main_state = state
        self.main_state.register_observer(self.refresh)
        self.threshold = None
        self.contour_number = None

        vertical_layout = QVBoxLayout()

        # process parameters
        self.params_layout = QHBoxLayout()

        # threshold
        self.threshold_group_box = QGroupBox('Threshold')
        threshold_layout = QVBoxLayout()
        self.threshold_input = QSpinBox()
        self.threshold_input.setRange(0, 255)
        self.threshold_input.setSingleStep(5)
        self.threshold_input.valueChanged.connect(self.update_threshold)
        threshold_layout.addWidget(self.threshold_input)
        self.threshold_group_box.setLayout(threshold_layout)

        # contour number
        self.contour_number_group_box = QGroupBox('Contour Number')
        contour_number_layout = QVBoxLayout()
        self.contour_number_input = QSpinBox()
        self.contour_number_input.setRange(1, 10)
        self.contour_number_input.setSingleStep(1)
        self.contour_number_input.valueChanged.connect(self.update_contour_number)
        contour_number_layout.addWidget(self.contour_number_input)
        self.contour_number_group_box.setLayout(contour_number_layout)
        self.params_layout.addWidget(self.threshold_group_box)
        self.params_layout.addWidget(self.contour_number_group_box)
        self.params_layout.addStretch(1)

        vertical_layout.addLayout(self.params_layout, 0)

        # images layout
        self.images_layout = QHBoxLayout()
        self.preview_view = QLabel()
        self.corrected_view = QLabel()
        self.images_layout.addWidget(self.preview_view)
        self.images_layout.addWidget(self.corrected_view)
        vertical_layout.addLayout(self.images_layout, 1)

        # buttons layout
        button_layout = QHBoxLayout()
        back_button = QPushButton('Back', self)
        back_button.setMinimumWidth(200)
        back_button.setMaximumWidth(250)
        back_button.clicked.connect(self.back)
        self.next_button = QPushButton('Next', self)
        self.next_button.setMinimumWidth(200)
        self.next_button.setMaximumWidth(250)
        self.next_button.clicked.connect(self.next)
        button_layout.addWidget(back_button)
        button_layout.addWidget(self.next_button)
        vertical_layout.addLayout(button_layout, 0)

        self.setLayout(vertical_layout)

    def resizeEvent(self, event):
        """Override resize event to resize image while maintaining aspect ratio."""
        self.update_layout()
        super().resizeEvent(event)

    def next(self):
        corrected_file_name = get_new_filename(self.state.current_image())
        success = cv2.imwrite(corrected_file_name, self.images[1])

        if success:
            print(f"Image saved successfully at {corrected_file_name}")
        else:
            print("Failed to save the image.")

        if not self.state.is_last_image():
            self.state.update_current_image_params(TransformParams(self.threshold, self.contour_number))
            self.state.next_image()
        else:
            exit(0)

    def back(self):
        if not self.state.is_first_image():
            self.state.previous_image()
        else:
            self.main_state.show_confirmation()

    # listens to when the main gui changes over
    def refresh(self, state):
        self.state = ProcessGuiState(state)
        self.update_process_gui()

    def update_process_gui(self):
        params = self.state.current_image_params()
        self.threshold_input.setValue(params.threshold)
        self.contour_number_input.setValue(params.contour_number)

        if self.state.is_last_image():
            self.next_button.setText('Exit')

        current_image = self.state.current_image()
        self.images = find_and_correct_perspective(current_image, params.threshold, params.contour_number)
        self.update_layout()

    def update_layout(self):
        image_width = int(self.width() * 0.5)
        param_width = int(image_width * 0.5)

        self.threshold_group_box.setMaximumWidth(param_width)
        self.contour_number_group_box.setMaximumWidth(param_width)
        self.preview_view.setMaximumWidth(image_width)
        self.corrected_view.setMaximumWidth(image_width)

        if self.images is not None:
            self.preview_view.setPixmap(convert_cv_qt(self.preview_view, self.images[0]))
            self.corrected_view.setPixmap(convert_cv_qt(self.corrected_view, self.images[1]))

    def update_threshold(self, state):
        self.threshold = state

    def update_contour_number(self, state):
        self.contour_number = state
