import cv2

camera_capture = cv2.VideoCapture(0)

fps = 30

size = (int(camera_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(camera_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

video_writer = cv2.VideoWriter('out/video.avi', cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)

success, frame = camera_capture.read()

num_frames_remaining = 10 * fps - 1

while success and num_frames_remaining > 0:
    video_writer.write(frame)
    success, frame = camera_capture.read()

    num_frames_remaining -= 1