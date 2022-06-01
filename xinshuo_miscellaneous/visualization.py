# Author: Xinshuo Weng
# email: xinshuo.weng@gmail.com
import colorsys
import sys
from typing import List

from skvideo.io import FFmpegWriter

from xinshuo_miscellaneous.file_io import mkdir_if_missing, load_list_from_folder, load_image
from xinshuo_miscellaneous.image_processing import image_resize


def random_colors(N, bright=True):
    """
    Generate random colors.
    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    """
    brightness = 1.0 if bright else 0.7
    hsv = [(i / float(N), 1, brightness) for i in range(N)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    # random.shuffle(colors)
    return colors


def generate_video_from_list(image_list: List[str], save_path, framerate: int = 30, downsample=1,
                             display=True, warning=True, debug=True):
    '''
    create video from a list of images with a framerate
    note that: the height and widht of the images should be a multiple of 2
    parameters:
        image_list:			a list of image path
        save_path:			the path to save the video file
        framerate:			fps
    '''
    if debug:
        assert framerate > 0, 'the framerate is a positive integer'
    mkdir_if_missing(save_path)
    inputdict = {'-r': str(framerate)}
    outputdict = {'-r': str(framerate), '-crf': '18', '-vcodec': 'libx264', '-profile:V': 'high', '-pix_fmt': 'yuv420p'}
    video_writer = FFmpegWriter(save_path, inputdict=inputdict, outputdict=outputdict)
    count = 1
    num_images = len(image_list)
    for image_path in image_list:
        if display:
            sys.stdout.write('processing frame %d/%d\r' % (count, num_images))
            sys.stdout.flush()
        image = load_image(image_path, resize_factor=downsample, warning=warning, debug=debug)

        # make sure the height and width are multiple of 2
        height, width = image.shape[0], image.shape[1]
        if not (height % 2 == 0 and width % 2 == 0):
            height += height % 2
            width += width % 2
            image = image_resize(image, target_size=[height, width], warning=warning, debug=debug)

        video_writer.writeFrame(image)
        count += 1

    video_writer.close()


def generate_video_from_folder(images_dir, save_path, framerate=30, downsample=1, depth=1, reverse=False, display=True, warning=True, debug=True):
    image_list, num_images = load_list_from_folder(images_dir, ext_filter=['.jpg', '.png', '.jpeg'], depth=depth, debug=debug)
    if reverse:
        image_list = image_list[::-1]
    if display:
        print('%d images loaded' % num_images)
    generate_video_from_list(image_list, save_path, framerate=framerate, downsample=downsample, display=display, warning=warning, debug=debug)
