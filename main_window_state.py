class MainWindowState:
    def __init__(self):
        self.images = []
        self.gui_index = 0
        self.update_observers = []

    def add_input_images(self, image_paths):
        for image_path in image_paths:
            self.images.append(image_path)
        self.show_confirmation()

    def show_confirmation(self):
        self.update_gui_index(1)

    def clear_input_images(self):
        self.images.clear()
        self.update_gui_index(0)

    def start_process(self):
        self.update_gui_index(2)

    def register_observer(self, observer):
        self.update_observers.append(observer)

    def update_gui_index(self, index):
        self.gui_index = index
        for observer in self.update_observers:
            observer(self)
