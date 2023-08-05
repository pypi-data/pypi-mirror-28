import numpy as np


def apply_nonlinearity(h):
    """Applies ReLU on each element of h.
        h -- 3D numpy array, each plane contains the output of a neuron for all possible input pair
             ReLU:
                0 if h <= 0
                h if h > 0
        Thresholds the negative values in the input array to 0.
    """

    low_values_flags = h < 0  # Where values are low
    h[low_values_flags] = 0  # All low values set to 0



#########################################################
#                       TESTS                           #
#########################################################

# TEST 1
# Example with array containing positive numbers
# print("\n***** TEST 1 *****\n")
# trial1 =  np.ones((3,3,3))
# print("Before apply_nonlinearity:\n", trial1)
# nonl_trial1 = apply_nonlinearity(trial1)
# print("\nAfter apply_nonlinearity:\n", trial1)


# # TEST 2
# # Complicated example (positive and negative numbers as well)
# print("\n\n***** TEST 2 *****\n")
# trial2 = np.zeros((3,3,3))
# for i in range(0,3):
#     for j in range(0, 3):
#         for k in range(0, 3):
#             trial2[i][j][k] = i/2+j/3-k
#
# print("Before apply_nonlinearity:\n", trial2)
# apply_nonlinearity(trial2)
# print("After apply_nonlinearity:\n", trial2)