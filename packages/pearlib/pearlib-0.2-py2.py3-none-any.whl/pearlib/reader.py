import numpy as np
import tensorflow as tf

def read_tensorflow_file(fname):
    new_graph = tf.Graph()

    with tf.Session(graph=new_graph) as sess:
        # Handles case where there is no .meta file
        try:
            saver = tf.train.import_meta_graph(fname + '.meta')
        except OSError:
            raise OSError("The .META file could not be found!")
            
        graph = tf.get_default_graph()

        # Handles the case where data is corrupted or missing
        try:
            tf.train.Saver().restore(sess, fname)
        except tf.errors.DataLossError:
            raise tf.errors.DataLossError(None, None, "A file is missing (.INDEX or .DATA), and the network could not be reconstructed, or the data is corrupted!")
        
        theta = []
        tmp = []
        tmpW = [0] * int(graph.get_collection_ref('trainable_variables').__len__() / 2)
        tmpb = [0] * int(graph.get_collection_ref('trainable_variables').__len__() / 2)

        file_writer = tf.summary.FileWriter(fname, sess.graph)

        for x in graph.get_collection_ref('trainable_variables'):
            if x.name[0] == 'W' or x.name[0] == 'b':
                if x.name[0] == 'W':
                    tmpW[int(x.name[1:-2]) - 1] = x.eval(sess)
                else:
                    tmpb[int(x.name[1:-2]) - 1] = x.eval(sess)
                    
    if tmpW.__len__() != tmpb.__len__():
        print("Missing data!")
        
    for x in range(tmpW.__len__()):
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
        raise ValueError("The network that was loaded in is empty! The input network you used probably does not follow our guidelines!")
    else:
        return theta
        


