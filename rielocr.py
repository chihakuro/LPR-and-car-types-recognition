#Import libraries
import cv2
from matplotlib import pyplot as plt
import numpy as np
import easyocr
import albumentations as A

def rielocr(img):
    # Define the augmentations
    blur = A.Blur(p=0.01, blur_limit=(3, 7))
    median_blur = A.MedianBlur(p=0.01, blur_limit=(3, 7))
    to_gray = A.ToGray(p=0.01)
    clahe = A.CLAHE(p=0.01, clip_limit=(1, 4.0), tile_grid_size=(8, 8))

    # Load the image
    image = cv2.imread(img)

    transformed = blur(image=image)
    transformed = median_blur(image=transformed['image'])
    transformed = to_gray(image=transformed['image'])
    transformed = clahe(image=transformed['image'])

    # Create an EasyOCR reader object
    reader = easyocr.Reader(['en'])

    # Read the text from the transformed image
    result = reader.readtext(transformed['image'])

    # Extract the text from the result
    text = ''.join([x[1] for x in result])         
    return text          
  

