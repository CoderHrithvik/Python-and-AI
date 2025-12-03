import cv2 
import numpy as np
def apply_filter(image, filter_type):
    """Apply the selected colour filter or edge detection."""
    # Create a copy of the image to avoid modyfing the original
    filtered_image = image.copy

    if filter_type == "red_tint":
        filtered_image[:, :, 1] = 0 # Green channel = 0
        filtered_image[:, :, 0] = 0 # Blue channel = 0
    elif filter_type == "green_tint":
        filtered_image[:, :, 0] = 0 # Blue channel = 0
        filtered_image[:, :, 2] = 0 # Red channel = 0
    elif filter_type == "blue_tint":
        filtered_image[:, :, 1] = 0
        filtered_image[:, :, 2] = 0
    elif filter_type == "sobel":
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
        combined_sobel = cv2.bitwise_or(sobelx.astype('uint8'), sobely.astype('uint8'))
        filtered_image = cv2.cvtColor(combined_sobel, cv2.COLOR_GRAY2BGR)

    return filtered_image
image_path = 'C:\Users\hrith\Desktop\AI and Python Codingal\tiger-2535888_1280.jpg'
image = cv2.imread(image_path)

if image is None:
    print("Error: Image not found!")
else:
    filter_type = "original"

    print("Press the following keys to apply filters:")
    print("r - Red Tint")
    print("g - Green Tint")
    print("b - Blue Tint")
    print("s - Sobel Edge Detection")
    print("c - Canny Edge Detection")
    print("q - Quit")

    while True:
        filterted_image = apply_filter(image, filter)