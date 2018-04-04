#!/usr/bin/env python3


import os

import matplotlib.pyplot as plt


flight = 'F50'

s = []
v = []
a = []

with open(os.path.join('data', flight, 'flight_data')) as f:

    for line in map(str.strip, f):

        print(line)

        if len(line.split('\t')) == 3:

            seconds, velocity, altitude = line.split('\t')

        else:
            seconds = line.split('\t')[0]

        s.append(int(seconds))

        if velocity:
            v.append(int(velocity))
        else:
            v.append(0)

        if altitude:
            a.append(float(altitude))
        else:
            a.append(0)

plt.plot(v)



plt.show()
