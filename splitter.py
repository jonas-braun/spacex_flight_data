#!/usr/bin/env python3


import os

import cv2


def crop_frame(img):


    panel = img[0:450, 1920-450:1920]

    timer = panel[10:60, :]

    telemetry = panel[140:280, 45:45+380]

    return timer, telemetry



def crop(folder):


    for filename in os.listdir(folder):

        img = cv2.imread(os.path.join(folder, filename))

        print(img.shape)

        panel = img[0:450, 1920-450:1920]

        cv2.imwrite(os.path.join('cropped', filename), panel)

        timer = panel[10:60, :]

        cv2.imwrite(os.path.join('timer', filename), timer)

        telemetry = panel[140:280, 45:45+380]

        cv2.imwrite(os.path.join('telemetry', filename), telemetry)




if __name__ == '__main__':

    folder = 'images'

    crop(folder)
