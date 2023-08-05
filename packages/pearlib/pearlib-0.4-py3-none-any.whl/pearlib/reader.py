import numpy as np
from tensorflow.python.training.saver import import_meta_graph, Saver
from tensorflow import errors
from tensorflow import Graph
from tensorflow import get_default_graph
from tensorflow import Session


def read_tensorflow_file(fname):
    """Read a TensorFlow file given with its filename.
            Return the parameters (weight matrix, bias) of the network.
    """
    new_graph = Graph()
    theta = []
    tmpW = []
    tmpb = []

    with Session(graph=new_graph) as sess:
        # Handles case where there is no .meta file
        try:
            import_meta_graph(fname + '.meta')
        except OSError:
            raise OSError("The .META file could not be found!")

        graph = get_default_graph()

        # Handles the case where data is corrupted or missing
        try:
            Saver().restore(sess, fname)
        except errors.DataLossError:
            raise errors.DataLossError(None, None,
                                       "A file is missing (.INDEX or .DATA), and the network could not be reconstructed, or the data is corrupted!")

        theta = []
        tmpW = [0] * int(len(graph.get_collection_ref('trainable_variables')) / 2)
        tmpb = [0] * int(len(graph.get_collection_ref('trainable_variables')) / 2)

        for x in graph.get_collection_ref('trainable_variables'):
            if x.name[0] == 'W' or x.name[0] == 'b':
                if x.name[0] == 'W':
                    tmpW[int(x.name[1:-2]) - 1] = x.eval(sess)
                else:
                    tmpb[int(x.name[1:-2]) - 1] = x.eval(sess)

    if len(tmpW) != len(tmpb):
        raise errors.DataLossError(None, None,
                                   "The data is corrupted, or the naming was improper!")

    for x in range(len(tmpW)):
        theta += [(tmpW[x], tmpb[x])]

    # Checking that an actual network was loaded in, and not an empty one
    empty = True
    error = []
    for i in range(0, len(theta)):
        error.append((0, 0))
    try:
        error == theta
    except Exception:
        empty = False

    if empty == True:
        raise ValueError(
            "The network that was loaded in is empty! The input network you used probably does not follow our guidelines!")
    else:
        return theta
