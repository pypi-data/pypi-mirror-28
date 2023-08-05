import numpy as np
from pearlib.layer import Layer
from pearlib.apply_nonlinearity import apply_nonlinearity
from pearlib.sigmoid import *


def calculate_output(layers, res, layer_idx):
    """Calculates the  output of the given layer for all the possible inputs of the network in size.

        layers -- Ordered list of layers.
                               (Weight matrices and bias vectors of the network.)
        res -- resolution of the plane
        layer_idx -- index of the layer, for which we want to determine the output

        The output is calculated in the following way:
            h_0 = apply_nonlinearity(W_0*x+b_0)
            h_i = apply_nonlinearity(W_i*h_{i-1}+b_i)   for i = 1..layer_idx
                for the last layer: sigmoid(W_i*h_{i-1}+b_i)

        Returns the output(s) of the queried layer in a 3D array, where each plane represents the output of one neuron.
    """

    if layer_idx >= len(layers):
        raise ValueError("layer_idx exceeds the number of layers in the network")

    # Generate input field - it is always 2 dimensional, [-1,1]x[-1,1]
    x = np.linspace(-1, 1, res[0])
    y = np.linspace(-1, 1, res[1])

    # Initialize h_new for the first layer
    h_new = np.zeros((layers[0].n_input, len(x) * len(y)))
    for i in range(0, len(x)):
        for j in range(0, len(y)):
            h_new[:, i * len(y) + j] = [x[i], y[j]]

    # For each layer 0..layer_idx
    for layer_i in range(0, layer_idx + 1):
        # Save the output of the previous layer/input of the current layer to h_old
        h_old = h_new

        # Calculate the layer's output
        del h_new
        h_new = layers[layer_i].calculate_layer_output_mat(h_old)

        # If it is not the output layer: apply the nonlinearity
        if layer_i != len(layers) - 1:
            apply_nonlinearity(h_new)
        # If it is the last layer apply sigmoid
        else:
            h_new = sigmoid(h_new)

        # Clear the input (it will be overwritten in the next iteration)
        del h_old

    # Convert the output of the layer in the above defined format
    h_new = np.reshape(h_new.transpose(), [len(x), len(y), h_new.shape[0]], 'C')

    # Return the output of the layer_idxth layer
    return h_new
