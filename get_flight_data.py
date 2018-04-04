#!/usr/bin/env python3


import os
import sys
import time

import cv2    # version 3.1


from . import extractor, splitter, telemetry_splitter, timer, timer_test, velocity, velocity_test, altitude, altitude_test


analyze_video(flight_number='F50'):
    """
    stream a video file and extract the telemetry data from it
    flight_number is the name of a folder in the 'data' directory
    """

    base_folder = os.path.join('data', flight_number)

    timer_classifier = timer_test.Timer()
    velocity_classifier = velocity_test.Velocity()
    altitude_classifier = altitude_test.Altitude()

    # remove file
    with open(os.path.join(base_folder, 'flight_data'), 'w') as f:
        f.write('')

    # go through frames in video, take every 5th frame
    for i, image in enumerate(extractor.get_frame(base_folder, 5)):

        print('step: {}'.format(i))

        timer_string = ''
        velocity_string = ''
        altitude_string = ''
        
        timer_img, telemetry_img = splitter.crop_frame(image)

        #cv2.imshow('timer', timer_img)

        digits = timer.get_time(timer_img)

        #for digit in digits:
        #    cv2.imshow('digit', digit)
        #    cv2.waitKey(0)

        if digits:

            timer_string = int(timer_classifier.recognize(digits))

            if timer_string >= 0:
                timer_string = timer_string//100 * 60 + timer_string % 100
            else:
                timer_string = timer_string//-100 * 60 + timer_string % -100

            print(timer_string)

            #cv2.waitKey(1000)

        velocity_img, altitude_img = telemetry_splitter.split(telemetry_img)

        digits = velocity.get_digits(velocity_img)

        if digits:

            result = velocity_classifier.recognize(digits)

            if result:
                velocity_string = int(result)

                print(velocity_string)

        digits = altitude.get_digits(altitude_img)

        if digits:

            result = altitude_classifier.recognize(digits)

            if result:
                altitude_string = float(result)
                print(altitude_string)

        # log data to file
        with open(os.path.join(base_folder, 'flight_data'), 'a') as f:
            f.write('{}\t{}\t{}\n'.format(timer_string, velocity_string, altitude_string))



if __name__ == '__main__':

    try:
        arg = sys.argv[1]
    except IndexError:
        arg = ''

    analyze_video(arg)
