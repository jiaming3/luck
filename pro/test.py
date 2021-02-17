#!/usr/bin/env python

from __future__ import division, print_function
from nxp_imu import IMU
import time
import math
import numpy as np

"""
accel/mag - 0x1f
gyro - 0x21
pi@r2d2 nxp $ sudo i2cdetect -y 1
    0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 1f
20: -- 21 -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
"""


def imu():
    imu = IMU(gs=4, dps=2000, verbose=True)
    header = 67
    print('-'*header)
    print("| {:17} | {:20} | {:20} |".format("Accels [g's]", " Magnet [uT]", "Gyros [dps]"))
    print('-'*header)
    accRaw = np.empty([1,3])
    magRaw = np.empty([1,3])
    RadToDeg = 360 / 2*math.pi

    for _ in range(1000):
        a, m, g = imu.get()
        print('| {:>5.2f} {:>5.2f} {:>5.2f} | {:>6.1f} {:>6.1f} {:>6.1f} | {:>6.1f} {:>6.1f} {:>6.1f} |'.format(
            a[0], a[1], a[2],
            m[0], m[1], m[2],
            g[0], g[1], g[2])
        )


        magRaw[0] = m[1]
        magRaw[1] = m[2]
        magRaw[2] = m[3]

        accRaw[0] = a[0]
        accRaw[1] = a[1]
        accRaw[2] = a[3]



        headingraw = math.atan2(magRaw[1], magRaw[0]) * RadToDeg

        xM = magRaw[0]
        yM = magRaw[1]
        zM = magRaw[2]
        xG = accRaw[0]
        yG = accRaw[1]
        zG = accRaw[2]

        pitch = math.atan2(xG, math.sqrt(yG * yG + zG * zG))
        roll = math.atan2(yG, zG)
        roll_print = roll * RadToDeg
        pitch_print = pitch * RadToDeg

        xM2 = xM * math.cos(pitch) + zM * math.sin(pitch)
        yM2 = xM * math.sin(roll) * math.sin(pitch) + yM * math.cos(roll) - zM * math.sin(roll) * math.cos(pitch)
        compheading = math.atan2(yM2, xM2) * RadToDeg

        compheading = compheading + 90
        if compheading <= 0 :
           compheading = compheading * -1

        elif compheading > 0 :
            compheading = 360 - compheading


        print("compheading: ", compheading)
        time.sleep(1)



    #print('-'*header)
    #print(' uT: micro Tesla')
    #print('  g: gravity')
    #print('dps: degrees per second')
    #print('')


def ahrs():
    print('')
    imu = IMU(verbose=True)
    header = 47
    print('-'*header)
    print("| {:20} | {:20} |".format("Accels [g's]", "Orient(r,p,h) [deg]"))
    print('-'*header)
    for _ in range(10):
        a, m, g = imu.get()
        r, p, h = imu.getOrientation(a, m)
        print('| {:>6.1f} {:>6.1f} {:>6.1f} | {:>6.1f} {:>6.1f} {:>6.1f} |'.format(a[0], a[1], a[2], r, p, h))
        time.sleep(0.50)
    print('-'*header)
    print('  r: roll')
    print('  p: pitch')
    print('  h: heading')
    print('  g: gravity')
    print('deg: degree')
    print('')


if __name__ == "__main__":
    try:
        ahrs()
        imu()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass

    print('Done ...')
