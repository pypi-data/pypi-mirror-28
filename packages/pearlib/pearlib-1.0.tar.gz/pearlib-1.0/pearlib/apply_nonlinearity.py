def apply_nonlinearity(h):
    """Applies ReLU on each element of h.
        h -- nD array
             ReLU:
                0 if h <= 0
                h if h > 0
        Thresholds the negative values in the input array to 0.
    """

    low_values_flags = h < 0  # Where values are low
    h[low_values_flags] = 0  # All low values set to 0
