import cv2
import numpy
import time


class CaptureManager(object):
    def __init__(self, capture, preview_wm=None, mirror_preview=False):
        self.preview_window_manager = preview_wm
        self.should_mirror_preview = mirror_preview

        self._capture = capture
        self._channel = 0
        self._entered_frame = False

        self._frame = None
        self._image_filename = None

        self._video_filename = None
        self._video_encoding = None
        self._video_writer = None

        self._start_time = None
        self._frames_elapsed = long(0)

        self._fps_estimate = None

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame = None

    @property
    def frame(self):
        if self._entered_frame and self._frame is None:
            _, self._frame = self._capture.retrieve(self.channel)
        return self._frame

    @property
    def is_writing_image(self):
        return self._image_filename is not None

    @property
    def is_writing_video(self):
        return self._video_filename is not None

    def enter_frame(self):
        assert not self._entered_frame, 'Previous entered frame had no matching exit frame.'

        if self._capture is not None:
            self._entered_frame = self._capture.grab()

    def __enter__(self):
        self.enter_frame()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit_frame()

    def exit_frame(self):
        if self.frame is None:
            self._entered_frame = False
            return

        if self._frames_elapsed == 0:
            self._start_time = time.time()
        else:
            time_elapsed = time.time() - self._start_time
            self._fps_estimate = self._frames_elapsed / time_elapsed

        self._frames_elapsed += 1

        if self.preview_window_manager is not None:
            if self.should_mirror_preview:
                frame = numpy.fliplr(self._frame).copy()
            else:
                frame = self._frame

            self.preview_window_manager.show(frame)


        if self.is_writing_image:
            cv2.imwrite(self._image_filename, self._frame)
            self._image_filename = None

        self._write_video_frame()

        self._frame = None
        self._entered_frame = False

    def write_image(self, filename):
        self._image_filename = filename

    def start_writing_video(self, filename, encoding=cv2.VideoWriter_fourcc('I', '4', '2', '0')):
        self._video_filename = filename
        self._video_encoding = encoding

    def stop_writing_video(self):
        self._video_encoding = None
        self._video_filename = None
        self._video_writer = None

    def _write_video_frame(self):
        if not self.is_writing_video:
            return

        if self._video_writer is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps == 0.0:
                if self._frames_elapsed < 20:
                    return
                else:
                    fps = self._fps_estimate
            size = (int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self._video_writer = cv2.VideoWriter(self._video_filename, self._video_encoding, fps, size)

        self._video_writer.write(self._frame)


class WindowManager(object):
    def __init__(self, name, callback=None):
        self.callback = callback
        self._name = name
        self._is_window_created = False

    @property
    def is_window_created(self):
        return self._is_window_created

    def create_window(self):
        cv2.namedWindow(self._name)
        self._is_window_created = True

    def show(self, frame):
        cv2.imshow(self._name, frame)

    def destroy_window(self):
        cv2.destroyWindow(self._name)
        self._is_window_created = False

    def process_event(self):
        keycode = cv2.waitKey(1)
        if self.callback is not None and keycode != -1:
            keycode &= 0xFF
            self.callback(keycode)

