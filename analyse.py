import cv2


def is_contour_touching_border(contour, img_width, img_height, border_margin=10):
    # Check if any point of the contour is within the border_margin of the image borders
    for point in contour:
        x, y = point.ravel()
        if x <= border_margin or x >= img_width - border_margin or y <= border_margin or y >= img_height - border_margin:
            return True
    return False


def get_largest_contour(image, threshold=40):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply binary thresholding
    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Image dimensions
    img_height, img_width = image.shape[:2]

    # Find the largest contour by area that has 4 vertices
    largest_contour = None
    max_area = 0
    for cnt in contours:
        if not is_contour_touching_border(cnt, img_width, img_height):
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
            area = cv2.contourArea(cnt)
            if len(approx) == 4 and area > max_area:
                largest_contour = approx
                max_area = area

    # If a suitable contour was found
    if largest_contour is not None:
        return largest_contour
    else:
        return None
