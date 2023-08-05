import numpy as np


def sigmoid(x):
    """Applies the sigmoid function to the input"""
    return 1 / (1 + np.exp(-x))
