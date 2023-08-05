def get_color_for_layeridx(layeridx):
    """For an index it gives back an associated color (3 channel, each between 0 and 1)"""

    # For the first six layer: base colors
    if layeridx < 6:
        base6_colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1]]
        return base6_colors[layeridx]
    # From the 7th index: calculate a unique color
    else:
        # increment in red component
        ro = 161
        # increment in blue component
        bo = 111
        # increment in green component
        go = 67
        # maximum color
        nc = 256.0
        if layeridx % 3 == 0:
            return [((layeridx - 5) * ro % nc) / nc, ((layeridx - 6) * bo % nc) / nc, ((layeridx - 6) * go % nc) / nc]
        elif layeridx % 3 == 1:
            return [((layeridx - 6) * ro % nc) / nc, ((layeridx - 5) * bo % nc) / nc, ((layeridx - 6) * go % nc) / nc]
        else:
            return [((layeridx - 6) * ro % nc) / nc, ((layeridx - 6) * bo % nc) / nc, ((layeridx - 5) * go % nc) / nc]
