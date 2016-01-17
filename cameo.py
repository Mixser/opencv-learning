import cv2
from managers import CaptureManager, WindowManager


class Cameo(object):
    def __init__(self):
        self._window_manager = WindowManager('Cameo', self.on_keypress)

        self._capture_manager = CaptureManager(cv2.VideoCapture(0), self._window_manager, False)

    def run(self):
        self._window_manager.create_window()
        while self._window_manager.is_window_created:

            with self._capture_manager as f:
                frame = f.frame
            self._window_manager.process_event()

    def on_keypress(self, keycode):
        if keycode == 27:
            self._window_manager.destroy_window()


if __name__ == '__main__':
    Cameo().run()