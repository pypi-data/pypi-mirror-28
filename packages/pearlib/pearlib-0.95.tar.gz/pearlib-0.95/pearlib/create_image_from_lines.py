import numpy as np
from pearlib.draw_line import draw_line
from pearlib.layer import *
from pearlib.sigmoid import *


def create_image_from_lines(line_list, layer_indices, res = None, img = None, network = None , plot_output = False):
    """Generates the image with the boundary lines.
        -- line_list: contains all the lines from all the layers (list of lists)
        -- layer_indices: indicates which layers we would like to draw
        -- res: resolution of the plane ([n_col, n_row])
        -- img: optional. If given, the lines will be plotted on that image. If given, its resolution is used.
        -- network: The network object. Only used when plot output is true
        -- plot_output: optional. If true, the network should be given as well.
            If true, the background of the image will be the output of the neuron in the last layer
    """

    # Tests for the pair-inputs
    # If neither img nor res is given -> error, we do not know the resolution
    if img is None and res is None:
        raise ValueError("No resolution specified")
    # If the network is not given -> error, we can not calculate the output
    if network is None and plot_output:
        raise ValueError("No network is given to calculate the output image.")

    # If we should plot the network's output, get it
    if plot_output:
        # If in the last layer we truly have only 1 neuron
        layers = network.get_layers()
        if layers[(len(layers) - 1)].n_neurons == 1:
            # Get the output of the last layer
            all_output = network.get_all_output()
            # Copy the output of the last layer to be the background
            img = np.array(all_output[len(all_output) - 1], copy = True)
            # Expand the image to be colored
            img = np.tile(img, (1, 1, 3))
        # If in the last layer we have more than one neuron
        else:
            raise ValueError("Error in create_image_from_lines: The number of neurons in the last layer should be one.")

    # If plot_output is False
    else:
        # If the image is not given -> create it with the given resolution (each element is 1 (white))
        if img is None:
            x = np.linspace(-1, 1, res[0])
            y = np.linspace(-1, 1, res[1])
            img = np.ones((len(x), len(y), 3))

        # If the image is given
        else:
            # If the image is grayscale (has only 1 channel)
            if len(img.shape) == 2 or img.shape[2] == 1:
                img = np.transpose(img)
                img = img[:, :, np.newaxis]
                img = np.tile(img, (1, 1, 3))
            # If the image is colored (has 3 channels)
            elif img.shape[2] == 3:
                img = np.transpose(img, (1, 0, 2))
            # If the image has 4 channels, it is an RGBA image -> drop the fourth channel       
            elif img.shape[2] == 4:       
                img = img[:, :, :3]       
                img = np.transpose(img, (1, 0, 2))
            else:
                raise ValueError("The given image is neither a grayscale nor a colored RGB image\n"
                                 "(Does not have 1 nor 3 channels)")

    # For all the layers in layer_indices, draw the boundary lines
    for i in range(len(layer_indices)):
        # If it is not the last layer
        if layer_indices[i] < len(line_list):
            # for all the lines in the given layer
            for j in range(len(line_list[layer_indices[i]])):
                # draw the line to the image
                draw_line(img, line_list[layer_indices[i]][j])

    img = np.transpose(img, (1, 0, 2))
    return img
