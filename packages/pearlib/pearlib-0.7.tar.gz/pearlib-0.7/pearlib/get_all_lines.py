from pearlib.get_lines_from_layer_output import*
from pearlib.get_color_for_layeridx import *
from pearlib.network import *


def get_all_lines(network):
    """Stores and returns an array containing all the boundary lines for all layers.
       -- network: network object (containing the outputs of the layers in itself)
        Output: If we had n layers: n long list. The list contains lists of lines.
            The list ith element is a list, containing the boundary lines for the ith layer (if the ith layer contained
            m_i neurons, the list is m_i long.)
    """
    # Get the outputs of the layers in the network
    all_output = network.get_all_output()
    all_lines = []

    # For each layer
    for i in range(len(all_output)):
        # Get the lines from it
        lines = get_lines_from_layer_output(network, i, get_color_for_layeridx(i))
        # Append them to the all_lines array
        all_lines.append(list(lines))

    return all_lines
