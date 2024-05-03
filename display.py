import cv2
import ctypes


# Function to get screen resolution
def get_screen_resolution():
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    return screen_width, screen_height


# Function to display image in a window that fits within the screen resolution
def display_image(title, image):
    # Get the screen resolution
    screen_width, screen_height = get_screen_resolution()

    # Resize the image if it's larger than the screen resolution
    image_height, image_width, _ = image.shape
    if image_width > screen_width or image_height > screen_height:
        # Calculate the scaling factor to fit the image within the screen
        scale_factor = min(screen_width / image_width, screen_height / image_height)
        new_width = int(image_width * scale_factor)
        new_height = int(image_height * scale_factor)
        image = cv2.resize(image, (new_width, new_height))

    # Create a window and display the image
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)  # WINDOW_NORMAL allows resizing the window
    cv2.imshow(title, image)

