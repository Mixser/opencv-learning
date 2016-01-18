
def is_gray(image):
    return image.ndim < 3


def width_height_devided_by(image, divisor):
    h, w = image.shape[:2]
    return w / divisor, h / divisor


