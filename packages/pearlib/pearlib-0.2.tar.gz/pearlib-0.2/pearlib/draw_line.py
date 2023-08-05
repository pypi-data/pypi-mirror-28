import numpy as np
from pearlib.line import Line

# Why are the imports unused?...


def draw_line(img, line):
    """Draw the line given in 'line' on 'img'."""
    print("\n--Function draw_line starts...\n")

    # For each pixel indicated in line we set the img to its color.
    # TODO there should be a better way than do it pixel by pixel
    for i in range(0, line.points.shape[1]):
        idx = line.points[:, i]
        img[idx[0], idx[1], :] = line.color

    # print function end - debug
    print("\n--Function draw_line ends...\n")




# TODO
#######################################################
#                       TESTS                         #
#######################################################
