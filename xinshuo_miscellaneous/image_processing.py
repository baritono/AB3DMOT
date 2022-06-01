import cv2
import numpy as np
from PIL import Image

from xinshuo_miscellaneous.type_check import isnparray, isnannparray, isscalar, isimsize
from xinshuo_miscellaneous.math import safe_angle


def ispilimage(image_test):
    return isinstance(image_test, Image.Image)


def iscolorimage_dimension(image_test):
    '''
    dimension check for RGB color images (or RGBA)
    '''
    if ispilimage(image_test): image_test = np.array(image_test)
    return isnparray(image_test) and image_test.ndim == 3 and (image_test.shape[2] == 3 or image_test.shape[2] == 4)


def isgrayimage_dimension(image_test):
    '''
    dimension check for gray images
    '''
    if ispilimage(image_test): image_test = np.array(image_test)
    return isnparray(image_test) and (image_test.ndim == 2 or (image_test.ndim == 3 and image_test.shape[2] == 1))


def isimage_dimension(image_test):
    '''
    dimension check for images
    '''
    return iscolorimage_dimension(image_test) or isgrayimage_dimension(image_test)


def isuintimage(image_test):
    '''
    value check for uint8 images
    '''
    if ispilimage(image_test): image_test = np.array(image_test)
    if not isimage_dimension(image_test): return False
    return image_test.dtype == 'uint8'		# if uint8, must in [0, 255]


def isfloatimage(image_test):
    '''
    value check for float32 images
    '''
    if ispilimage(image_test): image_test = np.array(image_test)
    if not isimage_dimension(image_test): return False
    if not image_test.dtype == 'float32': return False

    item_check_le = (image_test <= 1.0)
    item_check_se = (image_test >= 0.0)
    return bool(item_check_le.all()) and bool(item_check_se.all())


def isnpimage(image_test):
    '''
    check if it is an uint8 or float32 numpy valid image
    '''
    return isnparray(image_test) and (isfloatimage(image_test) or isuintimage(image_test))


def isimage(image_test):
    return isnpimage(image_test) or ispilimage(image_test)


def safe_image(input_image, warning=True, debug=True):
    '''
    return a numpy image no matter what format the input is
    make sure the output numpy image is a copy of the input image
    parameters:
        input_image:		pil or numpy image, color or gray, float or uint
    outputs:
        np_image:			numpy image, with the same color and datatype as the input
        isnan:				return True if any nan value exists
    '''
    if ispilimage(input_image): np_image = np.array(input_image)
    elif isnpimage(input_image): np_image = input_image.copy()
    else: assert False, 'only pil and numpy images are supported, might be the case the image is float but has range of [0, 255], or might because the data is float64'

    isnan = isnannparray(np_image)
    if warning and isnan: print('nan exists in the image data')

    return np_image, isnan


def image_resize(input_image, resize_factor=None, target_size=None, interp='bicubic', warning=True, debug=True):
    '''
    resize the image given a resize factor (e.g., 0.25), or given a target size (height, width)
    e.g., the input image has 600 x 800:
        1. given a resize factor of 0.25 -> results in an image with 150 x 200
        2. given a target size of (300, 400) -> results in an image with 300 x 400
    note that:
        resize_factor and target_size cannot exist at the same time
    parameters:
        input_image:		an pil or numpy image
        resize_factor:		a scalar
        target_size:		a list of tuple or numpy array with 2 elements, representing height and width
        interp:				interpolation methods: bicubic or bilinear
    outputs:
        resized_image:		a numpy uint8 image
    '''
    np_image, _ = safe_image(input_image, warning=warning, debug=debug)
    if isfloatimage(np_image): np_image = (np_image * 255.).astype('uint8')

    if debug:
        assert interp in ['bicubic', 'bilinear'], 'the interpolation method is not correct'
        assert (resize_factor is not None and target_size is None) or (
                    resize_factor is None and target_size is not None), 'resize_factor and target_size cannot co-exist'

    if target_size is not None:
        if debug: assert isimsize(target_size), 'the input target size is not correct'
        target_width, target_height = int(round(target_size[1])), int(round(target_size[0]))
        if target_width == np_image.shape[1] and target_height == np_image.shape[0]: return np_image
    elif resize_factor is not None:
        if debug: assert isscalar(resize_factor) and resize_factor > 0, 'the resize factor is not a scalar'
        if resize_factor == 1: return np_image  # no resizing
        height, width = np_image.shape[:2]
        target_width, target_height = int(round(resize_factor * width)), int(round(resize_factor * height))
    else:
        assert False, 'the target_size and resize_factor do not exist'

    if interp == 'bicubic':
        resized_image = cv2.resize(np_image, (target_width, target_height), interpolation=cv2.INTER_CUBIC)
    elif interp == 'bilinear':
        resized_image = cv2.resize(np_image, (target_width, target_height), interpolation=cv2.INTER_LINEAR)
    else:
        assert False, 'interpolation is wrong'

    return resized_image


def image_rotate(input_image, input_angle, warning=True, debug=True):
    '''
    rotate the image given an angle in degree (e.g., 90). The rotation is counter-clockwise

    parameters:
        input_image:		an pil or numpy image
        input_angle:		a scalar, counterclockwise rotation in degree
    outputs:
        rotated_image:		a numpy uint8 image
    '''
    if debug: assert isscalar(input_angle), 'the input angle is not a scalar'
    rotation_angle = safe_angle(input_angle, warning=warning, debug=True)  # ensure to be in [-180, 180]
    np_image, _ = safe_image(input_image, warning=warning, debug=debug)
    if input_angle == 0:
        return np_image

    if isfloatimage(np_image):
        np_image = (np_image * 255.).astype('uint8')
    pil_image = Image.fromarray(np_image)
    if rotation_angle != 0:
        pil_image = pil_image.rotate(rotation_angle, expand=True)
    rotated_image = np.array(pil_image).astype('uint8')

    return rotated_image
