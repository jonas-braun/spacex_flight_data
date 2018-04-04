#!/usr/bin/env python3


import os
import string

import numpy as np

import cv2



class Altitude():

    width = 18
    height = 24

    model_path = 'models'

    def __init__(self):

        self.samples = np.load(os.path.join(self.model_path, 'altitude_samples.npy'))
        self.labels = np.load(os.path.join(self.model_path, 'altitude_labels.npy'))
        
        self.model = cv2.ml.KNearest_create()
        self.model.train(self.samples, cv2.ml.ROW_SAMPLE, self.labels)

    def recognize(self, digits):

        string_ = ''

        for img in digits:

            roi = img[0:self.height,0:self.width]  #, 0]

            h, w = roi.shape

            img = np.pad(roi, ((0,self.height-h), (0,self.width-w)), 'constant')

            img = np.array(img.reshape(1, self.width*self.height), dtype=np.float32)
            retval, results, neigh_resp, dists = self.model.findNearest(img, k = 1)
            char = chr(int(results[0][0]))

            string_ += char

        return self.clean(string_)


    def clean(self, string_):

        cleaned_string = ''

        for char in string_:

            if char in ['.']:
                cleaned_string += char

            elif char in string.digits:
                cleaned_string += char

        return cleaned_string


if __name__ == '__main__':

    width = 18
    height = 24


    folder = '../data/telemetry/altitude'


    samples = np.load('altitude_samples.npy')
    labels = np.load('altitude_labels.npy')

    print(samples.shape)

    model = cv2.ml.KNearest_create()

    model.train(samples, cv2.ml.ROW_SAMPLE, labels)



    for filename in os.listdir(folder):

        string = ''

        path = os.path.join(folder, filename, 'digits')

        for image_filename in sorted(os.listdir(path)):

            img = cv2.imread(os.path.join(path, image_filename))    # uint8

            roi = img[0:height,0:width, 0]

            h, w = roi.shape

            img = np.pad(roi, ((0,height-h), (0,width-w)), 'constant')

            #img = np.array(img.flatten(), dtype=np.float32)
            img = np.array(img.reshape(1, width*height), dtype=np.float32)
     
            retval, results, neigh_resp, dists = model.findNearest(img, k = 1)


            char = chr(int(results[0][0]))

            #print(char)
            string += char

        with open(os.path.join(folder, filename, 'result'), 'w') as f:
            f.write(string)
