#####################################################
#####################################################
## PEAR: EXAMPLE FILE TO VISUALIZE NEURAL NETWORKS ##
#####################################################
#####################################################

import numpy as np
import matplotlib.pyplot as plt
from pearlib.network import Network
from pearlib.create_image import create_image
from pearlib.save_image import save_image
from pearlib.calculate_output import calculate_output
from pearlib.get_all_lines import get_all_lines
from pearlib.create_image_from_lines import create_image_from_lines

# Path of the network to load.
network_name = "./3000_parameters/lena.jpg"
# Initializing Pear's inner representation for networks
my_network = Network(network_name)

resolution = [301, 301]

# Extracting layers and computing all the outputs for the given resolution
layers = my_network.get_layers()
lines = get_all_lines(my_network)

fig, ax = plt.subplots()


###############################################################
# Case 1: visualizing the last layer on a blank background    #
###############################################################
image_from_scratch = create_image(my_network, [len(layers) - 2], resolution, None, False)

ax.imshow(image_from_scratch, cmap = 'gray' ,interpolation = 'nearest', origin = 'upper')


###############################################################
# Case 2: visualizing the last layer on approximated image    #
###############################################################
# This time, we will not recompute everything from scratch:
# we already have the lines, we just need to draw them
image_on_approximation = create_image_from_lines(lines, [len(layers) - 2], resolution, None, my_network, True)

fig, ax = plt.subplots()
ax.imshow(image_on_approximation, cmap = 'gray' ,interpolation = 'nearest', origin = 'upper')


###############################################################
# Case 3: visualizing the last layer on a background image    #
###############################################################
lena = plt.imread('./lena.jpg')
lena = lena / 255 # Normalizing

image_with_background = create_image(my_network, [len(layers) - 2], None, lena, False)
fig, ax = plt.subplots()
ax.imshow(image_with_background, cmap = 'gray' ,interpolation = 'nearest', origin = 'upper')


plt.show()


##############################################################
# Saving a created image to the current folder               #
##############################################################
save_image('./test_lena.png', image_with_background)
