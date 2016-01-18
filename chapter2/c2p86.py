import cv2

clicked = False


def on_mouse(event, x, y, flags, param):
    global clicked
    if event == cv2.EVENT_LBUTTONUP:
        clicked = False

camera = cv2.VideoCapture(0)

cv2.namedWindow('Window')
cv2.setMouseCallback('Window', on_mouse)

success, frame = camera.read()

while success and cv2.waitKey(1) == -1 and not clicked:
    cv2.imshow('Window', frame)
    success, frame = camera.read()


cv2.destroyWindow('Window')