class Line:
    """Defines a boundary line object"""
    # Each column contains th ecoordinates of a point pf the line
    points = []
    # Color of the line (unique for each layer)
    color = [1, 1, 1]

    def __init__(self, _points=[], _color=[1,1,1]):
        self.points = _points
        self.color = _color
