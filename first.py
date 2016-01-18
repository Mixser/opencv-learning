import cv2
import numpy

image = cv2.imread('images/first.jpg')

b, g, r = cv2.split(image)
cv2.imwrite('out/first.png', cv2.merge((r, g, b)))