from pearlib.apply_nonlinearity import apply_nonlinearity
from pearlib.sigmoid import *

# Correctness should be checked by someone else as well
# there is no kind of error handling so far


def calculate_all_output(layers, res):
    """Calculates the  output of the layers for all the possible inputs of the network in size.

        layers ~ ([layer_i]) -- Ordered list of layers. All of them
                               Weight matrices and bias vectors of the network.
        res -- resolution of the plane

        The output is calculated in the following way:
            h_0 = apply_nonlinearity(W_0*x+b_0)
            h_i = W_i*h_{i-1}+b_i   for i = 1..layer_idx
            for the last layer: apply_sigmoid

        Returns the output(s) of all the layers in a list.
            the first element of this list is also a list, containing the outputs of the first layer, etc
    """

    # debug print
    print("--function calculate_all_output starts...")
    # TODO - Missing test if we really have enough (and the right) layer in theta and in layer_idx
    #   we can test the size of the weight matrices eg

    # TODO if the size is in wrong order (eg s_x1 > s_x2)

    # Generate input field - it is always 2 dimensional
    #   If the images have the size [-1,1]^2 then needs to be refine
    x = np.linspace(-1,1, res[0])
    y = np.linspace(-1,1, res[1])

    # Initialize h_new for the first layer
    h_new = np.zeros((layers[0].n_input, len(x)*len(y)))
    # TODO there should be a better way to do this...
    for i in range(0, len(x)):
        for j in range(0, len(y)):
            h_new[:,i*len(y)+j] = [x[i], y[j]]

    # print the input pairs - debug
    print("\nInput of the 0th layer\n", h_new)

    # Array containing the outputs
    all_output = []
    # For each layer
    for layer_i in range(0, len(layers)):
        # Save the output of the previous layer/input of the layer to h_old
        h_old = h_new

        # Calculate the layer's output
        del h_new
        h_new = layers[layer_i].calculate_layer_output_mat(h_old)

        # Print the output of the layer before ReLU - debug
        print("Output of layer ", layer_i, "before nonlinearity:\n",h_new)

        # If it is not the output layer: apply the nonlinearity
        if layer_i != len(layers)-1:
            apply_nonlinearity(h_new)
        # If it is the last layer
        else:
            h_new = sigmoid(h_new)
        # Clear the input (it will be overwritten in the next iteration)
        del h_old

        # Print the output of the layer - debug
        print("Output of layer ", layer_i, " after nonlinearity:\n",h_new)

        all_output.append(np.reshape(h_new.transpose(), [len(x), len(y), h_new.shape[0]], 'C'))

    # debug print
    print("\n--function calculate_all_output ends...\n")

    # Return all the outputs
    return all_output


#################################################
#                   TESTS                       #
#################################################

# TODO refresh the test according to the new size definition

# # TEST 1
# # 3layer network, predefined weights and biases
#
# # Define the first layer
# W0 = np.array([ [1, 0], [0, 1], [-1, 0], [0, -1] ])
# b0 = np.array([0, 0, 0, 0])
# c0 = [255, 0, 0]
# # Why does it run the whole layer.py file??
# l0 = Layer(W0, b0, c0)
#
# # Define the second layer
# W1 = np.array([ [1, 0, 0, 0], [0, 1, 0, 1], [1, 0, 1, 2]])
# b1 = np.array([ 0, 0, 0])
# c1 = [0, 255, 0]
# l1 = Layer(W1, b1, c1)
#
# # Define the third layer
# W2 = np.array([ [-1, 0, 0], [1, 1, 0]])
# b2 = np.array([ 0, 0])
# c2 = [0, 0, 255]
# l2 = Layer(W2, b2, c2)
#
# theta = []
# theta.append(l0)
# theta.append(l1)
# theta.append(l2)
# sizex1 = -2
# sizex2 = 2
# sizey1 = -3
# sizey2 = 3
# layer_idx1 = 2
# output = calculate_output(theta, [sizex1, sizey1, sizex2, sizey2], layer_idx1)
# print("Final output, along 3rd dim.")
# for z in range(0, output.shape[2]):
#     print("output[:,:,z]\n", output[:,:,z])