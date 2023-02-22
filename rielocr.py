#Import libraries
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr

def rielocr(Segs):
  #Load image
  img = cv2.imread(Segs)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # blur
  blur = cv2.GaussianBlur(gray, (0,0), sigmaX=33, sigmaY=33)

  # divide
  divide = cv2.divide(gray, blur, scale=255)

  # otsu threshold
  thresh = cv2.threshold(divide, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

  #Create an EasyOCR reader object:
  reader = easyocr.Reader(['en'])
  result = reader.readtext(thresh)

  text = ''
  range(len(result))
  for i in range(0,len(result)):
    text += result[i][-2]
    if i == range(len(result)-1):
      break
    else:
      text+='-'
  text = text[:-1]
  return text

