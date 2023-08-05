import numpy as np

# TODO: sign unused, do we need it?


class Line:
    # Each column contains the coordinates of a non-zero element
    points = []
    # Sign is unused so far
    sign = -1
    color = [1, 1, 1]

    def __init__(self, _points=[], _sign=-1, _color = [1,1,1]):
        self.points = _points
        self.sign = _sign
        self.color = _color


# TODO test