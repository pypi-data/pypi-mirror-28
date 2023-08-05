import numpy as np
from pearlib.line import Line
from pearlib.network import *


def get_lines_from_layer_output(network, layer_idx, linecolor = [1, 1, 1]):
    """
    From the output, calculate the boundary lines.
    -- network: network object (containing the outputs of its layer)
    -- layer_idx: index, indicates that from which layer we want to get the lines
    -- linecolor: color of the line (color of the layer in which this line is)
    Return a list of lines, containing a line object for each neuron in the layer.
    If the layer contained m neuron, lines will be m long.
    """


    all_output = network.get_all_output()
    if layer_idx > len(all_output):
        raise ValueError("The layer index exceeds the size of the network")

    # Get the output of the layer
    h = all_output[layer_idx]
    # Get the sign for each element
    signed_h = np.sign(h)
    # Create an array to store if the sign changes at a given point of the input or not
    h_conv = np.zeros_like(signed_h)

    # For each neuron separately
    for k in range(0, signed_h.shape[2]):
        # Search for sign change in columns: If the sign changes from [i,j-1] to [i,j] than h_conv at [i,j]
        #   will contain 0, otherwise h[i,j] = 1. We do not examine where j=0. (first column)
        for i in range(0, signed_h.shape[0]):
            for j in range(0, signed_h.shape[1]):
                # first column: skip, here we can not have the boundary
                if j == 0:
                    h_conv[i, j, :] = 1
                # j > 0
                else:
                    # If the sign does not change
                    if signed_h[i, j, k] == signed_h[i, j-1, k]:
                        h_conv[i,j,k] = 1
                    # if the sign changes
                    else:
                        h_conv[i, j, k] = 0

        # Search for sing change in rows: almost the same as with columns, but we compare [i-1, j] with [i,j]
        # We only overwrite the elements if the sign differs between the rows, we do not set to '1'
        #   any element which was marked as 'changing sign' ones during examining the columns.
        for j in range(0, signed_h.shape[1]):
            for i in range(0, signed_h.shape[0]):
                # if it is the first row -> skip
                if i == 0:
                    h_conv[i, j, :] = 1
                # if the sign differs: set to 0
                else:
                    if signed_h[i, j, k] != signed_h[i-1, j, k]:
                        h_conv[i, j, k] = 0

    lines = []
    # For each neuron (channel) find the zero elements in h_conv. Convert them to Line objects,
    #   and append these Line objects ordered to the lines list
    for k in range(0, h_conv.shape[2]):
        lines.append(Line(np.array(np.where(h_conv[:, :, k] == 0)), _color = linecolor))

    return lines
