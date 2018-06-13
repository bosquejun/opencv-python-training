from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__version__ = '0.0.1'
__author__ = 'jun-paul.i.bosque'


import cv2
import numpy as np


def apply_invert(frame):
    return cv2.bitwise_not(frame)
    

def apply_overlay(frame, filterOpt):
    f_height, f_width, f_channel = frame.shape
    overlay = np.full((f_height, f_width, 4), filterOpt, dtype='uint8')
    frame = cv2.addWeighted(overlay, 0.5, frame, 1.0, 0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    return frame

def apply_sepia(frame, intensity=0.5):
    blue,green,red = 20,66,120
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    sepia_bgra = (blue, green, red, 1)
    return apply_overlay(frame, sepia_bgra)

def apply_sepia_custom(frame, intensity=0.5):
    blue,green,red = 255,120,60
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    sepia_bgra = (blue, green, red, 1)
    return apply_overlay(frame, sepia_bgra)

def captureVideo():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        cv2.imshow('invert', apply_invert(frame))
        cv2.imshow('speia', apply_sepia(frame))
        cv2.imshow('custom_speia', apply_sepia_custom(frame))
        if cv2.waitKey(1) == 27:
            break;
    cap.release()
    cv2.destroyAllWindows()


captureVideo()
