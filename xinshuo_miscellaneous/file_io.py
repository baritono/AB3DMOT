# Author: Xinshuo Weng
# email: xinshuo.weng@gmail.com

# this file contains a set of function for manipulating file io in python
import os, glob, glob2

from PIL.Image import Image
from xinshuo_miscellaneous.type_check import is_path_exists_or_creatable, is_path_exists, isfolder, isinteger
from xinshuo_miscellaneous.image_processing import image_rotate, image_resize


def safe_path(input_path, warning=True, debug=True):
    '''
    convert path to a valid OS format, e.g., empty string '' to '.', remove redundant '/' at the end from 'aa/' to 'aa'
    parameters:
    	input_path:		a string
    outputs:
    	safe_data:		a valid path in OS format
    '''
    if debug:
        assert isinstance(input_path, str), 'path is not a string: %s' % input_path
    return os.path.normpath(input_path)


def fileparts(input_path, warning=True, debug=True):
    '''
    this function return a tuple, which contains (directory, filename, extension)
    if the file has multiple extension, only last one will be displayed

    parameters:
        input_path:     a string path

    outputs:
        directory:      the parent directory
        filename:       the file name without extension
        ext:            the extension
    '''
    good_path = safe_path(input_path, debug=debug)
    if len(good_path) == 0: return ('', '', '')
    if good_path[-1] == '/':
        if len(good_path) > 1:
            return (good_path[:-1], '', '')  # ignore the final '/'
        else:
            return (good_path, '', '')  # ignore the final '/'

    directory = os.path.dirname(os.path.abspath(good_path))
    filename = os.path.splitext(os.path.basename(good_path))[0]
    ext = os.path.splitext(good_path)[1]
    return (directory, filename, ext)


def mkdir_if_missing(input_path, warning=True, debug=True):
    '''
    create a directory if not existing:
        1. if the input is a path of file, then create the parent directory of this file
        2. if the root directory does not exists for the input, then create all the root directories recursively until the parent directory of input exists

    parameters:
        input_path:     a string path
    '''
    good_path = safe_path(input_path, warning=warning, debug=debug)
    if debug: assert is_path_exists_or_creatable(good_path), 'input path is not valid or creatable: %s' % good_path
    dirname, _, _ = fileparts(good_path)
    if not is_path_exists(dirname): mkdir_if_missing(dirname)
    if isfolder(good_path) and not is_path_exists(good_path): os.mkdir(good_path)


def load_list_from_folder(folder_path, ext_filter=None, depth=1, recursive=False, sort=True, save_path=None, debug=True):
    '''
    load a list of files or folders from a system path

    parameters:
        folder_path:    root to search
        ext_filter:     a string to represent the extension of files interested
        depth:          maximum depth of folder to search, when it's None, all levels of folders will be searched
        recursive:      False: only return current level
                        True: return all levels till to the input depth

    outputs:
        fulllist:       a list of elements
        num_elem:       number of the elements
    '''
    folder_path = safe_path(folder_path)
    if debug: assert isfolder(folder_path), 'input folder path is not correct: %s' % folder_path
    if not is_path_exists(folder_path):
        print('the input folder does not exist %s\n' % folder_path)
        return [], 0
    if debug:
        assert isinstance(recursive, bool), 'recursive should be a logical variable: {}'.format(recursive)
        assert depth is None or (isinteger(depth) and depth >= 1), 'input depth is not correct {}'.format(depth)
        assert ext_filter is None \
               or (isinstance(ext_filter, list) and all(isinstance(ext_tmp, str) for ext_tmp in ext_filter))\
               or isinstance(ext_filter, str), 'extension filter is not correct'
    if isinstance(ext_filter, str):
        ext_filter = [ext_filter]                               # convert to a list
    # zxc

    fulllist = list()
    if depth is None:        # find all files recursively
        recursive = True
        wildcard_prefix = '**'
        if ext_filter is not None:
            for ext_tmp in ext_filter:
                # wildcard = os.path.join(wildcard_prefix, '*' + string2ext_filter(ext_tmp))
                wildcard = os.path.join(wildcard_prefix, '*' + ext_tmp)
                curlist = glob2.glob(os.path.join(folder_path, wildcard))
                if sort: curlist = sorted(curlist)
                fulllist += curlist
        else:
            wildcard = wildcard_prefix
            curlist = glob2.glob(os.path.join(folder_path, wildcard))
            if sort: curlist = sorted(curlist)
            fulllist += curlist
    else:                    # find files based on depth and recursive flag
        wildcard_prefix = '*'
        for index in range(depth-1): wildcard_prefix = os.path.join(wildcard_prefix, '*')
        if ext_filter is not None:
            for ext_tmp in ext_filter:
                # wildcard = wildcard_prefix + string2ext_filter(ext_tmp)
                wildcard = wildcard_prefix + ext_tmp
                curlist = glob.glob(os.path.join(folder_path, wildcard))
                if sort: curlist = sorted(curlist)
                fulllist += curlist
            # zxc
        else:
            wildcard = wildcard_prefix
            curlist = glob.glob(os.path.join(folder_path, wildcard))
            # print(curlist)
            if sort: curlist = sorted(curlist)
            fulllist += curlist
        if recursive and depth > 1:
            newlist, _ = load_list_from_folder(folder_path=folder_path, ext_filter=ext_filter, depth=depth-1, recursive=True)
            fulllist += newlist

    fulllist = [os.path.normpath(path_tmp) for path_tmp in fulllist]
    num_elem = len(fulllist)

    # save list to a path
    if save_path is not None:
        save_path = safe_path(save_path)
        if debug: assert is_path_exists_or_creatable(save_path), 'the file cannot be created'
        with open(save_path, 'w') as file:
            for item in fulllist: file.write('%s\n' % item)
        file.close()

    return fulllist, num_elem


def load_txt_file(file_path, debug=True):
    '''
    load data or string from text file
    '''
    file_path = safe_path(file_path)
    if debug: assert is_path_exists(file_path), 'text file is not existing at path: %s!' % file_path
    with open(file_path, 'r') as file: data = file.read().splitlines()
    num_lines = len(data)
    file.close()
    return data, num_lines


def save_txt_file(data_list, save_path, debug=True):
    '''
    save a list of string to a file
    '''
    save_path = safe_path(save_path)
    if debug: assert is_path_exists_or_creatable(save_path), 'text file is not able to be created at path: %s!' % save_path

    first_line = True
    with open(save_path, 'w') as file:
        for item in data_list:
            if first_line:
                file.write('%s' % item)
                first_line = False
            else: file.write('\n%s' % item)
    file.close()


def load_image(src_path, resize_factor=None, target_size=None, input_angle=0, gray=False, warning=True, debug=True):
    '''
    load an image from given path, with preprocessing of resizing and rotating, output a rgb image
    parameters:
        resize_factor:      a scalar
        target_size:        a list or tuple or numpy array with 2 elements, representing height and width
        input_angle:        a scalar, counterclockwise rotation in degree
    output:
        np_image:           an uint8 rgb numpy image
    '''
    src_path = safe_path(src_path, warning=warning, debug=debug)
    if debug: assert is_path_exists(src_path), 'image path is not correct at %s' % src_path
    if resize_factor is None and target_size is None: resize_factor = 1.0           # default not to have resizing

    with open(src_path, 'rb') as f:
        with Image.open(f) as img:
            if gray: img = img.convert('L')
            else:
                try:
                    img = img.convert('RGB')
                except IOError:
                    print(src_path)
            np_image = image_rotate(img, input_angle=input_angle, warning=warning, debug=debug)
            np_image = image_resize(np_image, resize_factor=resize_factor, target_size=target_size, warning=warning, debug=debug)
    return np_image