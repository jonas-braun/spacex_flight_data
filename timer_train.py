#!/usr/bin/env python3


import os

import numpy as np

import cv2



model_folder = '../models/'

labels_dict = {}
with open(os.path.join(model_folder, 'timer_training_labels')) as f:
    for line in map(str.strip, f):
        id_, label = line.split('\t')
        labels_dict[id_] = label

#print(labels_dict)


width = 19
height = 26


folder = os.path.join(model_folder, 'timer_training')

n_samples = len(os.listdir(folder))
n_samples = len(labels_dict)

samples = np.empty((n_samples,width*height), dtype=np.float32)
labels = np.empty((n_samples, 1), dtype=np.float32)

for i, filename in enumerate(os.listdir(folder)):

    id_ = filename.split('.')[0]


    labels[i] = ord(labels_dict[id_])


    img = cv2.imread(os.path.join(folder, filename))    # uint8

    roi = img[0:height,0:width, 0]

    h, w = roi.shape

    img = np.pad(roi, ((0,height-h), (0,width-w)), 'constant')

    samples[i] = img.flatten()



model = cv2.ml.KNearest_create()

model.train(samples, cv2.ml.ROW_SAMPLE, labels)

#retval, results, neigh_resp, dists = model.find_nearest(roismall, k = 1)


np.save(os.path.join(model_folder, 'timer_samples.npy'), samples)
np.save(os.path.join(model_folder, 'timer_labels.npy'), labels)




