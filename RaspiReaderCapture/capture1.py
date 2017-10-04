"""
capture1.py
"""
"""
capture images from two pi cameras
"""

import RPi.GPIO as gp
import os
from picamera import PiCamera
from time import sleep
import sys
sys.path.append('./lib')
from transform_fingerprint import process_print
import numpy as np
import cv2
import thread

COLOR_FILEPATH = 'color.png'
FITR_FILEPATH = 'ftir.png'
MATCHING_FILEPATH = 'matching.png'

num_threads = 0
thread_started = False
lock = thread.allocate_lock()
output_buffers = [np.empty((2592 * 1952 * 3,), dtype=np.uint8),
                  np.empty((2592 * 1952 * 3,), dtype=np.uint8)]

camera = PiCamera()
camera.vflip = True
camera.resolution = (2592, 1944)

gp.setwarnings(False)
gp.setmode(gp.BOARD)

#led pins
gp.setup(36, gp.OUT)
gp.setup(38, gp.OUT)
gp.setup(40, gp.OUT)

#camera pins
gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)
gp.output(11, True)
gp.output(12, True)

def main():
    # turn on lights
    lights(True)

    # camera capture
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)
    print("starting first capture")
    try:
        capture(1)
        print("finished capturing 1")
    except Exception as e:
        print(e)
        lights(False)

    print("starting second capture")
    gp.output(7, False)
    gp.output(11, True)
    gp.output(12, False)
    try:
        capture(2)
        print("finished capturing 2")
    except Exception as e:
        print(e)
        lights(False)
    lights(False) # turn of leds
    # now write out the captured buffers to disk
    output_buffer1 = output_buffers[0].reshape((1952, 2592, 3))
    output_buffer1 = output_buffer1[:1944, :2592, :]
    output_buffer2 = output_buffers[1].reshape((1952, 2592, 3))
    output_buffer2 = output_buffer2[:1944, :2592, :]
    matching_image = process_print(output_buffer2)
    # crop out images before sending
    output_buffer1 = output_buffer1[:, 1160:2450, :]
    output_buffer2 = output_buffer2[:, 350:1800, :]
    thread.start_new_thread(writeImage, (output_buffer1, COLOR_FILEPATH))
    thread.start_new_thread(writeImage, (output_buffer2, FITR_FILEPATH))
    cv2.imwrite(MATCHING_FILEPATH, matching_image)
    while not thread_started:
        pass
    while num_threads > 0:
        pass

def writeImage(img_buffer, img_name):
    global num_threads, thread_started
    # thread is starting, place a lock
    lock.acquire()
    num_threads += 1
    thread_started = True
    lock.release()
    # do work
    cv2.imwrite(img_name, img_buffer)
    # finish thread
    lock.acquire()
    num_threads -= 1
    lock.release()

def capture(cam):
    camera.contrast = 50 if cam == 2 else 0
    sleeptime = 1.5 if cam == 1 else .5
    
    try:
        sleep(sleeptime)
        camera.capture(output_buffers[cam-1], 'bgr')
    except Exception as e:
        print(str(e))
        lights(False)
    

def lights(switch):
    if switch:
        gp.output(36, gp.HIGH)
        gp.output(38, gp.HIGH)
        gp.output(40, gp.HIGH)
    else:
        gp.output(36, gp.LOW)
        gp.output(38, gp.LOW)
        gp.output(40, gp.LOW)

if __name__ == "__main__":
    main()

    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)
    lights(False)
    print("exiting...")
