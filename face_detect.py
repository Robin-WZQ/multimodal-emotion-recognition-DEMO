# -*- coding: UTF-8 -*-

import sys,os,dlib,glob,numpy
from skimage import io
import cv2


def show_face(path):
    '''
    show the detected(analysis) face
        args:
            path: video path
    '''

    detector = dlib.get_frontal_face_detector()
    capture = cv2.VideoCapture(path)

    while True:
        red,video_frame = capture.read()
        dets = detector(video_frame, 1)
        if len(dets)>=1:
            for d in dets:
                cropped = video_frame[dlib.rectangle.top(d):dlib.rectangle.bottom(d),dlib.rectangle.left(d):dlib.rectangle.right(d)]
                cv2.imwrite("detected.png",cropped)
                break
            break
    capture.release()

#if __name__=='__main__':
#   show_face("sadness.mp4")
