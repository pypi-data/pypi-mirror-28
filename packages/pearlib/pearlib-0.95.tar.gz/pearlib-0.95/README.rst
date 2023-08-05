Pear
And neural networks appear


Pear is a library that aims at offering a visual representation of neural networks. It can read networks built using Google's TensorFlow in and, for each requested layer, draw the associated decision boundaries.

Pear is still in the development process.

Installing Pear will also install the following packages (if they are not already installed on your system): numpy, Pillow, matplotlib, tensorflow, webcolors.

To use, do::
	>>> import pearlib

Pear is not yet able to work will all types of network: only networks with 2 inputs and 1 output are accepted so far. Moreover, to simplify the parameters extraction, the input networks must follow the following naming convention:

- All weight matrices should be named "W" followed by the number of the layer they belong to. Example: the weight matrix of the first layer will be called "W1".
- All bias vectors should be named "b" followed by the number of the layer they belong to. Example: the bias vector of the first layer will be called "b1".

Example networks for Lena, with different numbers of parameters are available in the "example" folder, as well as an example running file "example.py" showing how to use Pear to visualize your network.


A graphical user interface for Pear is available for download here: https://lc.cx/gPgP
To start it, unzip the file and do in your command terminal::
	>>> python3 main.py