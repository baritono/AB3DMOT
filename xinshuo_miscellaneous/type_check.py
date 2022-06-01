# Author: Xinshuo Weng
# email: xinshuo.weng@gmail.com

# this file includes functions checking the datatype and equality of input variables
import os

import numpy as np


def isinteger(integer_test):
    if isinstance(integer_test, np.ndarray):
        return False
    try:
        return isinstance(integer_test, int) or int(integer_test) == integer_test
    except ValueError:
        return False
    except TypeError:
        return False


def isfloat(float_test):
    return isinstance(float_test, float)


def isscalar(scalar_test):
    try: return isinteger(scalar_test) or isfloat(scalar_test)
    except TypeError: return False


def islistoflist(list_test):
    if not isinstance(list_test, list):
        return False
    return all(isinstance(tmp, list) for tmp in list_test) and len(list_test) > 0


def isnparray(nparray_test):
    return isinstance(nparray_test, np.ndarray)


def isnannparray(nparray_test):
    return isnparray(nparray_test) and bool(np.isnan(nparray_test).any())


def is2dpts(pts_test):
    '''
    2d point coordinate, numpy array or list or tuple with 2 elements
    '''
    return (isnparray(pts_test) or isinstance(pts_test, list) or isinstance(pts_test, tuple)) \
           and np.array(pts_test).size == 2


def isimsize(size_test):
    '''
    shape check for images
    '''
    return is2dpts(size_test)


############################################################# path
# note:
#		empty path is not valid, a path of whitespace ' ' is valid
def is_path_valid(pathname):
    try:
        if not isinstance(pathname, str) or not pathname:
            return False
    except TypeError:
        return False
    else:
        return True


def is_path_creatable(pathname):
    '''
    if any previous level of parent folder exists, returns true
    '''
    if not is_path_valid(pathname): return False
    pathname = os.path.normpath(pathname)
    pathname = os.path.dirname(os.path.abspath(pathname))

    # recursively to find the previous level of parent folder existing
    while not is_path_exists(pathname):
        pathname_new = os.path.dirname(os.path.abspath(pathname))
        if pathname_new == pathname: return False
        pathname = pathname_new
    return os.access(pathname, os.W_OK)


def is_path_exists(pathname):
    try: return is_path_valid(pathname) and os.path.exists(pathname)
    except OSError: return False


def is_path_exists_or_creatable(pathname):
    try: return is_path_exists(pathname) or is_path_creatable(pathname)
    except OSError: return False


def isfolder(pathname):
    '''
    if '.' exists in the subfolder, the function still justifies it as a folder. e.g., /mnt/dome/adhoc_0.5x/abc is a folder
    if '.' exists after all slashes, the function will not justify is as a folder. e.g., /mnt/dome/adhoc_0.5x is NOT a folder
    '''
    if is_path_valid(pathname):
        pathname = os.path.normpath(pathname)
        if pathname == './': return True
        name = os.path.splitext(os.path.basename(pathname))[0]
        ext = os.path.splitext(pathname)[1]
        return len(name) > 0 and len(ext) == 0
    else: return False
