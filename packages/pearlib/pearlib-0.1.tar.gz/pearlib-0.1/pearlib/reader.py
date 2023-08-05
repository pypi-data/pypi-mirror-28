import numpy as np
import tensorflow as tf


def read_tensorflow_file(fname):
    new_graph = tf.Graph()

    with tf.Session(graph=new_graph) as sess:
        saver = tf.train.import_meta_graph(fname + '.meta')
        graph = tf.get_default_graph()

        tf.train.Saver().restore(sess, fname)
        theta = []  # [[0,0]]*int(graph.get_collection_ref('trainable_variables').__len__()/2)
        tmp = []
        tmpW = [0] * int(graph.get_collection_ref('trainable_variables').__len__() / 2)
        tmpb = [0] * int(graph.get_collection_ref('trainable_variables').__len__() / 2)

        # print(theta)
        file_writer = tf.summary.FileWriter(fname, sess.graph)

        for x in graph.get_collection_ref('trainable_variables'):
            # "Legacy code" Our measurements don't have the new naming convention, but I want to upload a version, which works for them.
            if x.name[0:8] == 'Variable_':
                if not tmp:
                    tmp += [x]
                    continue
                if tmp[0].shape[1] == x.shape[0]:
                    theta += [(np.array(tmp[0].eval(sess)), np.array(x.eval(sess)))]
                    tmp = []
            # End of legacy
            if x.name[0] == 'W' or x.name[0] == 'b':
                if x.name[0] == 'W':
                    tmpW[int(x.name[1:-2]) - 1] = x.eval(sess)
                else:
                    tmpb[int(x.name[1:-2]) - 1] = x.eval(sess)
    if tmpW.__len__() != tmpb.__len__():
        print("Missing data!")
    for x in range(tmpW.__len__()):
        theta += [(tmpW[x], tmpb[x])]
    return theta


