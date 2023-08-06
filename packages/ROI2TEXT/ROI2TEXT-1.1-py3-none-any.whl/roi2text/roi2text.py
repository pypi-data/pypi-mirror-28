
'''
Quickly extract text from your screenshot into clipboard

Author: Yunik Maharjan
'''

from PIL import Image, ImageEnhance
import numpy as np
from scipy import ndimage
import pytesseract
from pynput import mouse
import pyscreenshot as ImageGrab
import subprocess
x_pos_start = 0
y_pos_start = 0

x_pos_end = 0
y_pos_end = 0


def unit_test(text):
    return text


def on_click(x, y, button, pressed):
    if pressed:
        # print(button == 'Button.left')
        global x_pos_start, y_pos_start
        x_pos_start = x
        y_pos_start = y

    else:
        global x_pos_end, y_pos_end
        x_pos_end = x
        y_pos_end = y
        # Stop listener
        return False


def clipboard(str):

    p = subprocess.Popen(['xsel', '-bi'], stdin=subprocess.PIPE)
    p.communicate(input=str.encode())


def enhance(im):
    sharp = ImageEnhance.Sharpness(im)
    img = sharp.enhance(1.5)
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(1.5)
    img.save('final1.jpg')
    return img


def faster_bradley_threshold(image, threshold=88, window_r=4):
    percentage = threshold / 100.
    window_diam = 2 * window_r + 1

    img = np.array(image).astype(np.float)
    # matrix of local means with scipy
    means = ndimage.uniform_filter(img, window_diam)

    # result: 0 for entry less than percentage*mean, 255 otherwise
    height, width = img.shape[:2]
    result = np.zeros((height, width), np.uint8)   # initially all 0
    result[img >= percentage * means] = 255
    # convert back to PIL image
    return Image.fromarray(result)


def blackornot(im):
    black_thresh = 50
    pixels = im.getdata()
    nblack = np.sum(np.array(pixels) < black_thresh)
    n = len(pixels)

    if (nblack / float(n)) > 0.8:
        return 1
    else:
        return 0


def main():

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    img = ImageGrab.grab(bbox=(x_pos_start, y_pos_start,
                               x_pos_end, y_pos_end))

    # im = np.asarray(img.convert(mode='L')).copy()
    img = img.convert(mode='L')

    value = blackornot(img)
    # print(value)
    if not value:
        im = faster_bradley_threshold(img)

    else:
        im = enhance(img)

    # print(x_pos_start, y_pos_start, x_pos_end, y_pos_end)

    TEXT = pytesseract.image_to_string(im)
    clipboard(TEXT)


if __name__ == "__main__":

    main()
