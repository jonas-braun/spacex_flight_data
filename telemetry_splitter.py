#!/usr/bin/env python3


import os

import cv2



def split(img):

        velocity = img[50:100, :190]

        altitude = img[50:100, 191:]

        return velocity, altitude



if __name__ == '__main__':

    folder = '../data/telemetry'

    raw_path = os.path.join(folder, 'raw')

    velocity_path = os.path.join(folder, 'velocity_raw')
    altitude_path = os.path.join(folder, 'altitude_raw')

    for filename in os.listdir(raw_path):


        img = cv2.imread(os.path.join(raw_path, filename))

        print(img.shape)

        velocity = img[50:100, :190]

        cv2.imwrite(os.path.join(velocity_path, filename), velocity)

        altitude = img[50:100, 191:]

        cv2.imwrite(os.path.join(altitude_path, filename), altitude)

