#!/usr/bin/env python3


import os

import random


import cv2


folder = '../data/telemetry/altitude/'
training_folder = '../data/telemetry/altitude_training'

for filename in os.listdir(folder):

    path = os.path.join(folder, filename, 'digits')

    for image_filename in os.listdir(path):

        img = cv2.imread(os.path.join(path, image_filename))

        cv2.imshow('digit', img)

        key = cv2.waitKey(0)

        id_ = hash(random.random())%10**8

        cv2.imwrite(os.path.join(training_folder, '{}.tiff'.format(id_)), img)

        char = chr(key)

        with open('altitude_training_labels', 'a') as f:
            f.write('{}\t{}\n'.format(id_, char))
