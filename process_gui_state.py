from dataclasses import dataclass


@dataclass
class TransformParams:
    threshold: int
    contour_number: int


class ProcessGuiState:
    def __init__(self, main_state):
        self.main_state = main_state
        self.image_index = 0
        self.update_observers = []
        self.image_params = {}

    def is_first_image(self):
        return self.image_index == 0

    def is_last_image(self):
        return self.image_index == len(self.main_state.images) - 1

    def current_image(self):
        return self.main_state.images[self.image_index]

    def current_image_params(self):
        current = self.current_image()

        if current not in self.image_params:
            self.image_params[current] = TransformParams(21, 1)

        return self.image_params[current]

    def update_current_image_params(self, params):
        current = self.current_image()
        self.image_params[current] = params

    def next_image(self):
        self.image_index += 1
        # Loop back to the start if we reach the end
        self.image_index %= len(self.main_state.images)
        self.notify_observers()

    def previous_image(self):
        self.image_index -= 1
        # Loop back to the end if we reach the start
        self.image_index %= len(self.main_state.images)
        self.notify_observers()

    def register_observer(self, observer):
        self.update_observers.append(observer)

    def notify_observers(self):
        for observer in self.update_observers:
            observer(self)
