# Preprocess histopath. images
from __future__ import division
from PIL import Image
from keras.utils import np_utils

import numpy as np
import matplotlib.pyplot as plt
import glob
import pickle
import os

INPUT_DIMENSION = (308, 168)
OUTPUT_DIMENSION = INPUT_DIMENSION
INPUT_PIXELS = INPUT_DIMENSION[0] * INPUT_DIMENSION[1]

DATA_PATH = '../data/'

NUM_CLASSES = 20
IM_PER_CLASS = 48

RESIZE_WIDTH = 50
wperc = RESIZE_WIDTH / float(INPUT_DIMENSION[0])
#RESIZE_HEIGHT = int(float(INPUT_DIMENSION[1]) * float(wperc))
RESIZE_HEIGHT = 50
RESIZE_PIXELS = RESIZE_WIDTH * RESIZE_HEIGHT

# Create labeled list of files
# Also downscale
def load_patches(cat_vec=True):
    patches, labels = [], []
    for r, d, files in os.walk(DATA_PATH):
        for f in files:
            filename = DATA_PATH  + f
            im = Image.open(filename).convert('L')

            im = im.resize((RESIZE_WIDTH, RESIZE_HEIGHT), Image.ANTIALIAS) # downscale

            label = f[0]
            label = letter_to_int(label)
            labels.append(label)

            # Preprocessing things
            imp = np.asarray(im)
            imp = imp.reshape(-1,).astype('f')

            patches.append(imp/255)

            im.close()

    labels = np.asarray(labels)
    if cat_vec:
        labels = np_utils.to_categorical(labels, NUM_CLASSES)
    return np.squeeze(np.asarray(patches)), labels

# Divide sets into tr_perc % training data
# and 100 - tr_perc % validation
def divide_sets(tr_perc, data, labels):
    tr_size = int(tr_perc * IM_PER_CLASS)
    v_size = IM_PER_CLASS - tr_size

    training = []
    valid = []

    t_labels = []
    v_labels = []
    
    labeled_training = dict()

    if tr_size == 0 or v_size == 0:
        print "Empty data set .... !" 
        return

    class_means = []

    for c in range(0, NUM_CLASSES):
        starting_ind = IM_PER_CLASS * c
        class_act = []
        for i in range(0, tr_size):
            ex = data[starting_ind + i]
            ex_l = labels[starting_ind + i]
            training.append(ex)
            class_act.append(ex)
            t_labels.append(ex_l)
        for j in range(tr_size, IM_PER_CLASS):
            ex = data[starting_ind + j]
            ex_l = labels[starting_ind + j]
            valid.append(ex)
            v_labels.append(ex_l)

        class_means.append(class_act)

    class_means = np.average(class_means,axis=1)

    return np.asarray(training), np.asarray(valid), np.asarray(t_labels), np.asarray(v_labels), np.asarray(class_means)

# Pass in a list of labels
# Returns unique labels list
def grab_labels(labels):
    l = []
    for i in labels:
        if i not in l:
            l.append(i)

    return l

def letter_to_int(l):
    _alph = 'ABCDEFGHIJKLMNOPQRST'
    return next((i for i, _letter in enumerate(_alph) if _letter == l), None)

"""
p,l = load_patches()
t,l,tl,vl,d = divide_sets(0.7, p,l)
print d.shape
"""
