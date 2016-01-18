import cv2
import numpy
import scipy.interpolate


def create_curve_func(points):
    if points is None:
        return None

    num_points =len(points)

    if num_points < 2:
        return None

    xs, ys = zip(*points)

    if num_points < 4:
        kind = 'linear'

    else:
        kind = 'cubic'

    return scipy.interpolate.interp1d(xs, ys, kind, bounds_error=False)


def create_lookup_array(func, length=256):
    if func is None:
        return None

    lookup_array = numpy.empty(length)
    for i in xrange(length):
        func_i = func(i)
        lookup_array[i] = min(max(0, func_i), length - 1)

    return lookup_array


def apply_lookup_array(array, src, dst):
    if array is None:
        return
    dst[:] = array[src]


def create_composite_func(func0, func1):
    if func0 is None:
        return func1

    if func1 is None:
        return func0

    return lambda x: func0(func1(x))


def create_flat_view(array):
    flat_view = array.view()
    flat_view.shape = array.size

    return flat_view



