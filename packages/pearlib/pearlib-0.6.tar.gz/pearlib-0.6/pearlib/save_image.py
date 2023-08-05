import matplotlib.image as mpl


def save_image(img_name, img):
    """Saves an array as an image"""
    mpl.imsave(img_name, img)
