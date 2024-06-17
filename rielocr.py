import cv2
from matplotlib import pyplot as plt
import numpy as np
import easyocr
import albumentations as A

def rielocr(img):
    # Load the image
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Sobel X to detect vertical edges
    sobelx = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)

    # Thresholding to get binary image
    _, binary = cv2.threshold(sobelx, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Morphological transformations to close gaps
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 3))
    morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Show the contours
    image_copy = image.copy()
    cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 2)
    plt.imshow(cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB))

    # Filter out the possible license plates
    possible_plates = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        if 2 < aspect_ratio < 5:  # Typical license plate aspect ratio
            possible_plates.append((x, y, w, h))

    # Use EasyOCR to check for characters on the possible plates
    reader = easyocr.Reader(['en'])
    text = ""

    for (x, y, w, h) in possible_plates:
        plate = gray[y:y + h, x:x + w]
        transformed = cv2.resize(plate, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        transformed = cv2.GaussianBlur(transformed, (5, 5), 0)
        
        result = reader.readtext(transformed)
        
        for res in result:
            text += res[1] + " "

    if text == "":
        return "No license plate found"
    return text.strip()