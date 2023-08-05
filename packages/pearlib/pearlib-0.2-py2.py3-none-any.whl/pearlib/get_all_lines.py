from pearlib.get_lines_from_layer_output import*
from pearlib.get_color_for_layeridx import *
from pearlib.network import *


def get_all_lines(network):
    """Stores and returns an array containing all the boundary lines for all layers.
       network: network object (containing the outputs of the layers in itself)
    Output: If we had n layers: n long list. The list contains lists of lines.
    The list ith element is a list, containing the boundary lines for the ith layer (if the ith layer contained
        m_i neurons, the list is m_i long.)
    """
    all_output = network.get_all_output()
    all_lines = []

    # For each layer
    for i in range(len(all_output)):
        # get the lines from it
        lines = get_lines_from_layer_output(network, i, get_color_for_layeridx(i))
        all_lines.append(list(lines))

    return all_lines



############################################################
#                       TESTS                              #
############################################################

# Test 1
# # Constructing the test network
# # Define the first layer
# W0 = np.array([[1, 1], [1, -1]])
# b0 = np.array([0, 0])
# c0 = [255, 0, 0]
# l0 = Layer(W0, b0, c0)
#
# # # Define the second layer
# W1 = np.array([[2, 1], [1, 1], [0, 1]])
# b1 = np.array([0, 0, 0])
# c1 = [0, 255, 0]
# l1 = Layer(W1, b1, c1)
#
# # # Define the third layer
# W2 = np.array([[2, 1, 1]])
# b2 = np.array([0])
# c2 = [0, 0, 255]
# l2 = Layer(W2, b2, c2)
#
# # # Link the layers
# theta = []
# theta.append(l0)
# theta.append(l1)
# theta.append(l2)
#
# # [sizex1, sizex2] x [sizey1, sizey2]
# sizex1 = -2
# sizex2 = 2
# sizey1 = -2
# sizey2 = 2
# # The index of the layer we would like to draw
# layer_idx1 = 2
# # Right now you should select manually the neuron to visualize in the layer_idxth layer
# neuron_idx = 0
#
# all_lines_main = get_all_lines(theta, [sizex1, sizey1, sizex2, sizey2], layer_idx1)
#
# for i in range(0, len(all_lines_main)):
#     print("Lines in the ", i, "th layer:\n")
#     for j in range(len(all_lines_main[i])):
#         print("--", j, "th neuron:\n")
#         print(all_lines_main[i][j].points)
#

