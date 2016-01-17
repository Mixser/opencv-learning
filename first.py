import cv2
import numpy

image = cv2.imread('images/first.jpg')

array = numpy.array(image)

for line in array:
    for pixel in line:
        pixel[0], pixel[1], pixel[2] = pixel[2], pixel[1], pixel[0]

cv2.imwrite('out/first.png', array)