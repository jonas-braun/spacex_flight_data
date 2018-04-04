#!/usr/bin/env python3


import os

import cv2


def get_frame(folder, frequency, skip=0):


    video_folder = os.path.join(folder, 'video')
    filename = os.listdir(video_folder)[0]

    vid = cv2.VideoCapture(os.path.join(video_folder, filename))

    print('extracting')

    for i in range(10**6):

        ret, img = vid.read()

        if not ret:
            break

        if not i % frequency:

            if i//frequency < skip:
                continue

            yield img



def dump_frames(folder, frequency, skip=0):


    video_folder = os.path.join(folder, 'video')
    filename = os.listdir(video_folder)[0]
    print(filename)

    vid = cv2.VideoCapture(os.path.join(video_folder, filename))

    path = os.path.join(folder, 'images')
    try:
        os.makedirs(os.path.join(path))
    except OSError:
        pass


    for i in range(10**6):

        ret, img = vid.read()

        if not ret:
            break

        if not i % frequency:

            if i//frequency < skip:
                continue

            cv2.imwrite(os.path.join(path, 'image{}.tiff'.format(i//frequency)), img)


            

if __name__ == '__main__':

    dump_frames('../data/F50', 5, 190)
