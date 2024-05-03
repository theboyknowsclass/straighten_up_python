import cv2
import numpy as np

from analyse import get_largest_contour


def order_points(pts):
    # Initial sort by x-coordinate
    x_sorted = pts[np.argsort(pts[:, 0]), :]

    # Grab the left-most and right-most points
    left_most = x_sorted[:2, :]
    right_most = x_sorted[2:, :]

    # Sort the left-most according to their y-coordinates
    left_most = left_most[np.argsort(left_most[:, 1]), :]
    (tl, bl) = left_most

    # Now, sort the right-most according to their y-coordinates
    right_most = right_most[np.argsort(right_most[:, 1]), :]
    (tr, br) = right_most

    # Return the coordinates in top-left, top-right, bottom-right, and bottom-left order
    return np.array([tl, tr, br, bl], dtype="float32")


def four_point_transform(image, pts):
    # The dimensions of the new image are determined by the extents of the contour
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # Compute the width of the new image, which will be the maximum distance between bottom-right and bottom-left
    # x-coords or top-right and top-left x-coords
    width_a = np.linalg.norm(br - bl)
    width_b = np.linalg.norm(tr - tl)
    max_width = max(int(width_a), int(width_b))

    # Compute the height of the new image, which will be the maximum distance between the top-right and bottom-right
    # y-coords or the top-left and bottom-left y-coords
    height_a = np.linalg.norm(tr - br)
    height_b = np.linalg.norm(tl - bl)
    max_height = max(int(height_a), int(height_b))

    # The destination points are the corners of a rectangle based on the calculated dimensions
    dst = np.array([
        tl,
        [max_width + tl[0], tl[1]],
        [max_width + tl[0], max_height + tl[1]],
        [tl[0], max_height + tl[1]]
    ], dtype="float32")

    # Compute the straighten_up transform matrix and apply it
    matrix = cv2.getPerspectiveTransform(rect, dst)

    # Width and Height of the original image
    width, height = image.shape[1], image.shape[0]

    warped = cv2.warpPerspective(image, matrix, (width, height))

    return warped


def find_and_correct_perspective(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image could not be read. Check the file path.")
        return

    largest_contour = get_largest_contour(image)

    # If a suitable contour was found
    if largest_contour is not None:

        # Draw selected contour on the original image
        image_with_contour = cv2.drawContours(image.copy(), [largest_contour], -1, (0, 255, 0), 3)

        # Perform straighten_up correction
        corrected_image = four_point_transform(image, largest_contour.reshape(4, 2))

        # Return the original and corrected images
        return [image_with_contour, corrected_image]

    else:
        print("No suitable quadrilateral contour found.")
        return None