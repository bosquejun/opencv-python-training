from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__version__ = '0.0.1'
__author__ = 'jun-paul.i.bosque'


import cv2
import numpy as np


def apply_invert(frame):
    return cv2.bitwise_not(frame)


def apply_portraitmode(frame):
    frame = applyAlphaConvert(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
    blurred = cv2.GaussianBlur(frame, (21, 21), 0)
    blended = apply_blend(frame, blurred, mask)
    frame = cv2.cvtColor(blended, cv2.COLOR_BGRA2BGR)
    return frame


def apply_blend(frame1, frame2, mask):
    alpha = mask / 255.0
    blended = cv2.convertScaleAbs(frame1 * (1 - alpha) + (frame2 * alpha))
    return blended


def applyAlphaConvert(frame):
    try:
        frame.shape[3]
    except IndexError:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        return frame


def apply_overlay(frame, filterOpt):
    f_height, f_width, f_channel = frame.shape
    overlay = np.full((f_height, f_width, 4), filterOpt, dtype='uint8')
    frame = cv2.addWeighted(overlay, 0.5, frame, 1.0, 0)
    frame = applyAlphaConvert(frame)
    return frame


def apply_sepia(frame, intensity=0.5):
    blue, green, red = 20, 66, 120
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    sepia_bgra = (blue, green, red, 1)
    return apply_overlay(frame, sepia_bgra)


def apply_sepia_custom(frame, intensity=0.5):
    blue, green, red = 255, 120, 60
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    sepia_bgra = (blue, green, red, 1)
    return apply_overlay(frame, sepia_bgra)


def captureVideo():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        # cv2.imshow('invert', apply_invert(frame))
        # cv2.imshow('speia', apply_sepia(frame))
        # cv2.imshow('custom_speia', apply_sepia_custom(frame))
        cv2.imshow('portrait_mode', apply_portraitmode(frame))
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


captureVideo()
