from pearlib.apply_nonlinearity import apply_nonlinearity
from pearlib.sigmoid import *


def calculate_all_output(layers, res):
    """Calculates the  output of the layers for all the possible inputs of the network in size.

        layers ~ ([layer_i]) -- Ordered list of the network's layers. (Weight matrices and bias vectors)
        res -- resolution of the plane

        The output is calculated in the following way:
            h_0 = apply_nonlinearity(W_0*x+b_0)
            h_i = apply_nonlinearity(W_i*h_{i-1}+b_i)   for i = 1..layer_idx
                for the last layer: sigmoid(W_i*h_{i-1}+b_i)

        Returns the output(s) of all the layers in a list.
            the first element of this list is also a list, containing the outputs of the first layer, etc
    """

    # Generate input field - it is always 2 dimensional, [-1,1]x[-1,1]
    x = np.linspace(-1, 1, res[0])
    y = np.linspace(-1, 1, res[1])

    # Initialize h_new for the first layer
    h_new = np.zeros((layers[0].n_input, len(x) * len(y)))
    for i in range(0, len(x)):
        for j in range(0, len(y)):
            h_new[:, i * len(y) + j] = [x[i], y[j]]

    # Array containing the outputs
    all_output = []
    # For each layer
    for layer_i in range(0, len(layers)):
        # Save the output of the previous layer/input of the layer to h_old
        h_old = h_new

        # Calculate the current layer's output
        del h_new
        h_new = layers[layer_i].calculate_layer_output_mat(h_old)

        # If it is not the output layer: apply the nonlinearity
        if layer_i != len(layers) - 1:
            apply_nonlinearity(h_new)
        # If it is the last layer: apply sigmoid
        else:
            h_new = sigmoid(h_new)

        # Clear the input (it will be overwritten in the next iteration)
        del h_old

        all_output.append(np.reshape(h_new.transpose(), [len(x), len(y), h_new.shape[0]], 'C'))

    # Return all the outputs
    return all_output
