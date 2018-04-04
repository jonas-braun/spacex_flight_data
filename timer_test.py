#!/usr/bin/env python3


import os
import string

import numpy as np

import cv2



class Timer():

    width = 19
    height = 26

    model_path = 'models'

    def __init__(self):

        self.samples = np.load(os.path.join(self.model_path, 'timer_samples.npy'))
        self.labels = np.load(os.path.join(self.model_path, 'timer_labels.npy'))
        
        self.model = cv2.ml.KNearest_create()
        self.model.train(self.samples, cv2.ml.ROW_SAMPLE, self.labels)


    def recognize(self, digits):

        string = ''

        for img in digits:

            roi = img[0:self.height,0:self.width]  #, 0]

            h, w = roi.shape

            img = np.pad(roi, ((0,self.height-h), (0,self.width-w)), 'constant')

            img = np.array(img.reshape(1, self.width*self.height), dtype=np.float32)
            retval, results, neigh_resp, dists = self.model.findNearest(img, k = 1)
            char = chr(int(results[0][0]))

            string += char

        return self.clean(string)


    def clean(self, string_):

        cleaned_string = ''

        for char in string_:

            if char in ['+','-']:
                cleaned_string += char

            elif char in string.digits:
                cleaned_string += char

        if cleaned_string[:2] == '-+':
            cleaned_string = cleaned_string[1:]

        if '+' in cleaned_string:
            cleaned_string = ''.join([ x for x in cleaned_string if x != '-' ])

        return cleaned_string[:7]


if __name__ == '__main__':


    width = 19
    height = 26


    folder = 'timer'


    samples = np.load('samples.npy')
    labels = np.load('labels.npy')

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
