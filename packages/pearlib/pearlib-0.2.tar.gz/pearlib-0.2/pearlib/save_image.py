import numpy as np
import matplotlib.image as mpl


def save_image(img_name, img):
    """Saves a numpy array as an image"""
    mpl.imsave(img_name, img)