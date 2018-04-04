#!/usr/bin/env python3


import os

from operator import itemgetter

import numpy as np

import cv2


def get_digits(img):

    bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, gb = cv2.threshold(bw, 127, 255, cv2.THRESH_BINARY)


    img2, contours, hierarchy = cv2.findContours(gb, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    contours2 = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1:
            [x,y,w,h] = cv2.boundingRect(contour)

            if w > 50:
                continue
            if x < 1:
                continue
            if h > 48:
                continue
            if y+h > 135:
                continue

            for i, contour2 in enumerate(contours2):
                # check if lies inside
                x2,y2,w2,h2 = contour2

                if x<x2 and y<y2 and w>w2+x2-x and h>h2+y2-y:

                    contours2[i] = (x,y,w,h)
                    break
            else:
                contours2.append((x,y,w,h))

    if not contours2:
        return None

    width = max(contours2, key=itemgetter(2))[2]
    height = max(contours2, key=itemgetter(3))[3]


    digits = []

    for i, contour in enumerate(sorted(contours2, key=itemgetter(0))):

        x,y,w,h = contour

        roi = gb[y:y+h, x:x+w]

        roi = np.pad(roi, ((0,height-h), (0,width-w)), 'constant')

        digits.append(roi)

    return digits


if __name__ == '__main__':

    folder = '../data/telemetry/altitude_raw'


    for filename in os.listdir(folder):

        #DEBUG
        if False and filename != 'image30.tiff':
            continue

        name = filename.split('.')[0]

        path = os.path.join(folder, filename)


        img = cv2.imread(path)

        bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, gb = cv2.threshold(bw, 127, 255, cv2.THRESH_BINARY)

        #print(gb.shape)

        cv2.imwrite('gb.tiff', gb)


        img2, contours, hierarchy = cv2.findContours(gb, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            continue

        #print(contours)
        #print(len(contours))
        #print(hierarchy)

        #img2 = cv2.drawContours(img, contours[5], 0, (0,255,0), 3)
        #cv2.imwrite('contours.tiff', img2)


        contours2 = []

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1:
                [x,y,w,h] = cv2.boundingRect(contour)

                if w > 50:
                    continue
                if x < 1:
                    continue
                if h > 48:
                    continue
                if y+h > 135:
                    continue

                print(x,y,w,h)

                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)



                for i, contour2 in enumerate(contours2):
                    # check if lies inside
                    x2,y2,w2,h2 = contour2
                    #print(i)

                    #print(x, x2)
                    #print(y, y2)
                    #print(w, w2)
                    #print(h, h2)
                    #print('\n')

                    if x<x2 and y<y2 and w>w2+x2-x and h>h2+y2-y:

                        contours2[i] = (x,y,w,h)
                        print('found')
                        break
                else:

                    contours2.append((x,y,w,h))

                #cv2.imshow('digit', img)
                #key = cv2.waitKey(0)

        #print(contours2)
        if not contours2:
            continue

        width = max(contours2, key=itemgetter(2))[2]
        #print(width)
        height = max(contours2, key=itemgetter(3))[3]
        #print(height)

        #cv2.imwrite('contours.tiff', img)

        velocity_folder = '../data/telemetry/altitude'

        for i, contour in enumerate(sorted(contours2, key=itemgetter(0))):

            x,y,w,h = contour

            roi = gb[y:y+h, x:x+w]

            #print(roi.shape)
            
            roi = np.pad(roi, ((0,height-h), (0,width-w)), 'constant')

            #print(roi.shape)

            try:
                os.makedirs(os.path.join(velocity_folder, name, 'digits'))
            except:
                pass

            cv2.imwrite(os.path.join(velocity_folder, name, 'digits', '{}.tiff'.format(i)), roi)









