import cv2
import numpy

first_image = cv2.imread('images/diff_1.jpeg')
second_image = cv2.imread('images/diff_2.jpeg')

# first_gray = cv2.cvtColor(first_image, cv2.COLOR_BGR2GRAY)
# second_gray = cv2.cvtColor(second_image, cv2.COLOR_BGR2GRAY)

detector = cv2.AKAZE_create()

kp1, des1 = detector.detectAndCompute(first_image, None)
kp2, des2 = detector.detectAndCompute(second_image, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)

matches = sorted(matches, key=lambda x:x.distance)

out_img = cv2.drawMatches(first_image, kp1, second_image, kp2, matches[:10], None, flags=2)

cv2.imshow('Out',out_img)

cv2.waitKey(0)