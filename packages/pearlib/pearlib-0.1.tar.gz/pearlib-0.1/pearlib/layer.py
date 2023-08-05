import numpy as np

# MISSING: error checking
# Somehow we should control b. It must! have the shape (n_neurons, 1)
#   Maybe something with property, but I could not get it work at first
#   We should not be able to modify b! (and W) - except in the constructor

# In test 4 dimension mismatch, probably we should handle it... Or just be really careful
# DOES NOT WORK WITH SINGLE INPUT

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
        # convert the input to np.array
        input_vec = np.array(args)
        # Get rid of unwanted dimensions
        input_vec = input_vec.squeeze()
        # Check if the shape of the input is correct
        if input_vec.shape[0] != self.n_input:
            # TODO error handling
            print("Inputs not matching")
            return
        # return the output for e
        return np.matmul(self.W, input_vec) + self.b

##############################################################
#                       TESTS                                #
##############################################################

# # TEST 1
# Empty constructor - error since we do not have that
# l1 = Layer()
# print("W:\n", l1.W, "b:\n", l1.b)


# # TEST 2
# # A normal setter test
# l2 = Layer(np.array([(1,2), (2,3), (5,6)]), np.array([1,2,3]), [90, 60, 90])
# print("W:\n", l2.W, "\nb:\n", l2.b, "\ncolor:\n", l2.color)

# # TEST 3
# # Test for changing b - WE SHOULD NOT DO THAT! b SHOULD HAVE THE SHAPE DEFINED BEFORE
# l3 = Layer(np.array([[1,2], [2,3], [5,6]]), np.array([1,2,3]), [90, 60, 90])
# l3.b = np.array([4,5,6])
# print("W:\n", l3.W, "\nb:\n", l3.b, "\ncolor:\n", l3.color)


# # TEST 4
# # Calculation of output for a given easy example
# l4 = Layer(np.array([ [2, 1], [1, 2] ]), np.array([-2, -2]), [90, 60, 90])
# inp = np.array([[2, 2], [10, 10]])
# print(inp.shape)
# #inp = np.array([[2], [10]])
# out4 = l4.calculate_layer_output_mat(inp)
# expected = [[12, 12], [20, 20]]
# print("Output:\n", out4, "\nExpected:\n", expected)

# # TEST 5
# # Another test for output calculation with more input/output
# l5 = Layer(np.array([ [2, 0], [0, 2], [1, 0] ]), np.array([-2, -2, 0]))
# input5 = [[0,0,1,1], [0, 1, 0, 1]]
# out5 = l5.calculate_layer_output_mat(input5)
# print("Output:\n", out5)