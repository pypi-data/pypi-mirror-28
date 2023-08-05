from pearlib.reader import read_tensorflow_file
from pearlib.get_color_for_layeridx import get_color_for_layeridx
from pearlib.layer import Layer
from pearlib.calculate_all_output import calculate_all_output
from pearlib import get_all_lines # To avoid import conflicts with get_all_lines
import numpy as np


class Network:
    """Contains the structure a neural network given as an input."""

    def __init__(self, filename=None):
        """Create a new NetworkHandler object.
        A NetworkHandler object has four attributes:
        - a name "filename" (here, its full path without any extension)
        - parameters "theta" containing, for each layer, weight and bias
        - a list of layers "layers" containing Layer objects that correspond to a layer
        - all_outputs: a list containing the outputs of each layer - if it is calculated
        """
        if filename:
            self.__filename = filename
            self.__theta = read_tensorflow_file(self.__filename)
            self.__layers = self.create_layers(self.__theta)
            self.__all_output = []
            self.__all_lines = []
        else:
            self.__filename = ""
            self.__theta = []
            self.__layers = []
            self.__all_output = []
            self.__all_lines = []

    def create_layers(self, theta):
        """Given the parameters "theta" of a network, extract the layers and build Layer objects from them.
        """
        layers = []
        for i in range(0, len(theta)):
            color = get_color_for_layeridx(i)
            W = np.transpose(theta[i][0])
            b = np.transpose(theta[i][1])
            layers.append(Layer(W, b, color))
        return layers

    def calculate_all_output(self, res):
        self.__all_output = calculate_all_output(self.__layers, res)

    def compute_all_lines(self):
         # To avoid import errors, since * from network is imported in get_all_lines and there can be conflicts.
        self.__all_lines = get_all_lines.get_all_lines(self)

    def get_filename(self):
        return self.__filename

    def get_theta(self):
        return self.__theta

    def get_layers(self):
        return self.__layers

    def set_layer(self, layers):
        self.__layers = layers

    def get_all_output(self):
        return self.__all_output

    def get_lines(self):
        return self.__all_lines
