from pearlib.reader import read_tensorflow_file
from pearlib.get_color_for_layeridx import get_color_for_layeridx
from pearlib.layer import Layer
from pearlib.calculate_all_output import calculate_all_output
from pearlib import get_all_lines # To avoid import conflicts with get_all_lines
import numpy as np


class Network:
    """Contains the structure of a neural network given as input."""

    def __init__(self, filename=None):
        """Create a new Network object.
        A Network object has five attributes:
        - a name "filename" (here, its full path without any extension)
        - parameters "theta" containing, for each layer, weight and bias
        - a list of layers "layers" containing Layer objects that correspond to a layer
        - all_outputs: a list containing the outputs of each layer - if it is calculated
        - all_lines: a list containing the boundary lines of each neuron - if it is calculated
        """
        self.__filename = filename
        self.__theta = read_tensorflow_file(self.__filename)
        self.__layers = self.create_layers(self.__theta)
        self.__all_output = []
        self.__all_lines = []

    def create_layers(self, theta):
        """Given the parameters "theta" of a network, extract the layers and build Layer objects from them."""
        layers = []
        for i in range(0, len(theta)):
            color = get_color_for_layeridx(i)
            W = np.transpose(theta[i][0])
            b = np.transpose(theta[i][1])
            layers.append(Layer(W, b, color))
        return layers

    def compute_all_output(self, res):
        """Computes the output of each neuron of the networkand stores it in __all_output"""
        self.__all_output = calculate_all_output(self.__layers, res)

    def compute_all_lines(self):
        """Computes the boundary lines for each neuron of the network and stores it in __all_lines"""
        # To avoid import errors, since * from network is imported in get_all_lines and there can be conflicts.
        self.__all_lines = get_all_lines.get_all_lines(self)

    def get_filename(self):
        return self.__filename

    def get_theta(self):
        return self.__theta

    def get_layers(self):
        return self.__layers

    def get_all_output(self):
        return self.__all_output

    def get_lines(self):
        return self.__all_lines
