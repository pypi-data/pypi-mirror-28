from pearlib.get_all_lines import *
from pearlib.create_image_from_lines import *


def create_image(network, layer_indices, res = None, img = None, plot_output = False):
    """Generates the image with the boundary lines.
        -- network: The Network object representing the network
        -- layer_indices: indicates which layers we would like to draw
        -- res: resolution of the plane ([n_col, n_row])
        -- img: optional. If given, the lines will be plotted to that image. If given, its resolution is used
                for the output image
        -- plot_output: optional.
            If true, the background of the image will be the output of the neuron in the last layer
    """

    # If neither img nor res is given -> error, we do not know the resolution
    if img is None and res is None:
        raise ValueError("No resolution specified")

    # If img is given, we set res for the resolution of the image
    if img is not None:
        res = [img.shape[1], img.shape[0]]

    # Calculate the output of the network for the specified resolution
    network.compute_all_output(res)
    # Get the boundary lines
    network.compute_all_lines()
    all_the_lines = network.get_lines()

    # Return the created image
    return create_image_from_lines(all_the_lines, layer_indices, res = res, img = img, network = network, plot_output = plot_output)
