import numpy as np


class Layer:
    """Class for defining a layer with its weight matrix and bias vector"""
    W = []  # np.array!
    b = []  # np.array!
    n_neurons = 0
    n_input = 0
    color = [1,1,1]

    def __init__(self, _W, _b, _color):
        self.W = _W
        self.b = _b[:,np.newaxis]
        self.n_neurons = _W.shape[0]
        self.n_input = _W.shape[1]
        self.color = _color

    def calculate_layer_output_mat(self, *args):
        """Calculate the output of the layer for *args.
            args -- matrix containing n_input rows. Each column is treated as an input vector
            the result is the output of the layer for each input (for each column of args.)
        """
        # Convert the input to np.array
        input_vec = np.array(args)
        # Get rid of unwanted dimensions
        input_vec = input_vec.squeeze()
        # Check if the shape of the input is correct
        if input_vec.shape[0] != self.n_input:
            raise ValueError("The given input does not match the shape of the expected input of the network")

        # Calculate and return the output
        return np.matmul(self.W, input_vec) + self.b
