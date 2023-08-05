import numpy as np
from pearlib.line import Line


def draw_line(img, line):
    """Draw the line given in 'line' on 'img'."""
    # For each pixel indicated in line we set the img to its color.
    for i in range(0, line.points.shape[1]):
        idx = line.points[:, i]
        img[idx[0], idx[1], :] = line.color
