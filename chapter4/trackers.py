import cv2
import rects
import utils

from chapter3 import managers


class Face(object):
    def __init__(self):
        self.face_rect = None

        self.left_eye_rect = None
        self.right_eye_rect = None

        self.nose_rect = None
        self.mouth_rect = None


class FaceTracker(object):
    def __init__(self, scale_factor=1.2, min_neighbors=2,
                 flags=cv2.CASCADE_SCALE_IMAGE):

        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.flags = flags

        self._faces = []

        self._face_classifier = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt.xml')
        self._eye_classifier = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')
        self._nose_classifier = cv2.CascadeClassifier('cascades/haarcascade_mcs_nose.xml')
        self._mouth_classifier = cv2.CascadeClassifier('cascades/haarcascade_mcs_mouth.xml')


    @property
    def faces(self):
        return self._faces

    def update(self, image):
        self._faces = []

        if utils.is_gray(image):
            image = cv2.equalizeHist(image)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.equalizeHist(image, image)

        min_size = utils.width_height_devided_by(image, 8)
        face_rects = self._face_classifier.detectMultiScale(image,
                                                            self.scale_factor,
                                                            self.min_neighbors,
                                                            self.flags, min_size)

        if face_rects is not None:
            for face_rect in face_rects:
                face = Face()
                face.face_rect = face_rect
                x, y, w, h = face_rect

                search_rect = (x + w / 7, y, w * 2 / 7, h / 2)
                face.left_eye_rect = self._detect_one_object(self._eye_classifier, image, search_rect, 64)

                search_rect = (x + w * 4 / 7, y, w * 2 / 7, h / 2)
                face.right_eye_rect = self._detect_one_object(self._eye_classifier, image, search_rect, 64)

                search_rect = (x + w / 4, y + h /4, w / 2, h / 2)
                face.nose_rect = self._detect_one_object(self._nose_classifier, image, search_rect, 32)

                search_rect = (x + w / 6, y + h * 2 / 3, w * 2 / 3, h / 3)
                face.mouth_rect = self._detect_one_object(self._mouth_classifier, image, search_rect, 16)

                self._faces.append(face)

    def _detect_one_object(self, classifier, image, rect, image_size_to_min_size_ratio):
        x, y, w, h = rect
        min_size = utils.width_height_devided_by(image, image_size_to_min_size_ratio)
        sub_image = image[y:y + h, x: x + w]
        sub_rects = classifier.detectMultiScale(sub_image, self.scale_factor, self.min_neighbors, self.flags, min_size)

        if len(sub_rects) == 0:
            return None

        sub_x, sub_y, sub_w, sub_h = sub_rects[0]

        return x + sub_x, y + sub_y, sub_w, sub_h


    def draw_debug_rects(self, image):
        if utils.is_gray(image):
            face_color = 255
            left_eye_color = 255
            right_eye_color = 255
            nose_color = 255
            mouth_color = 255
        else:
            face_color = (255, 255, 255)

            left_eye_color = (0, 0, 255)
            right_eye_color = (0, 255, 255)

            mouth_color = (255, 0, 0)

            nose_color = (0, 255, 0)

        for face in self._faces:
            rects.outline_rect(image, face.face_rect, face_color)

            rects.outline_rect(image, face.left_eye_rect, left_eye_color)
            rects.outline_rect(image, face.right_eye_rect, right_eye_color)

            rects.outline_rect(image, face.nose_rect, nose_color)

            rects.outline_rect(image, face.mouth_rect, mouth_color)


class Cameo(object):
    def __init__(self):
        self._window_manager = managers.WindowManager('Cameo', self._on_keypress)
        self._capture_manager = managers.CaptureManager(cv2.VideoCapture(0), self._window_manager, True)

        self._face_tracker = FaceTracker()
        self._shoud_draw_debug_rects = False

    def run(self):
        self._window_manager.create_window()
        counter = 0
        while self._window_manager.is_window_created:
            with self._capture_manager as manager:
                frame = manager.frame
                self._face_tracker.update(frame)
                faces = self._face_tracker.faces

                # for face in faces:
                #     counter += 1
                #     x, y, w, h = face.face_rect

                    # cv2.imwrite('../out/face_{}.png'.format(counter), frame[y: y + h, x: x + w])
                self._face_tracker.draw_debug_rects(frame)

            self._window_manager.process_event()

    def _on_keypress(self, keycode):
        if keycode == 27:
            self._window_manager.destroy_window()


if __name__ == '__main__':
    Cameo().run()