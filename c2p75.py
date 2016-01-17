import cv2
import numpy
import os

random_byte_array = bytearray(os.urandom(120000))

num_array = numpy.array(random_byte_array)

gray_image = num_array.reshape(300, 400)

cv2.imwrite('out/first.png', gray_image)

color_image = num_array.reshape(100, 400, 3)
cv2.imwrite('out/first-2.png', color_image)




