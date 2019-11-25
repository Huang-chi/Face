import RPi.GPIO as gpio
import os, time
import cv2
import pygame, pygame.camera
from os import listdir
from os.path import isfile, isdir, join

###
from SavingImagesPi_v2 import *
from Lock_v2 import *
from lib.load import load_all_image
#from lib.verify_identity import *
###

# setting the path
file_path = "./RealTimeImages/EncodingImages/or_images"
files = listdir(file_path)

# gpio setting
gpio.setmode (gpio.BCM)
gpio.setwarnings(False)
gpio.setup(21, gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.setup (16, gpio.OUT)

# pygame to appear view

pygame.camera.init()
lst = pygame.camera.list_cameras()

cam = pygame.camera.Camera(lst[0], (640,480))
cam.start()

# load the all images
known_face_encodings, names = load_all_image(files, file_path)
input_state = 0
while True:

    frame = pygame.surfarray.array3d(cam.get_image()).swapaxes(0, 1)
    cv2.imshow("Frame", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    #input_state = gpio.input(21)
    if input_state == 0:
        print("start")
        time.sleep(0.5)
        #input_state = 1
        time.sleep(0.5)
        #input_state = gpio.input(21)
        if input_state == 0:
            input_state = 1
            image_array = []
            framet_2 = pygame.surfarray.array3d(cam.get_image()).swapaxes(0, 1)
            framet_3 = pygame.surfarray.array3d(cam.get_image()).swapaxes(0, 1)
            image_array.append(frame)
            image_array.append(framet_2)
            image_array.append(framet_3)
            

            print("Enter Lock function:")
            open_or_close = Lock(image_array,known_face_encodings,names)
            if open_or_close > 1:
                print("open")
                gpio.output (16, gpio.HIGH)
                time.sleep (3)
                gpio.output (16, gpio.LOW)
        else:
            print("Enter SavingImages function:")
            SavingImages(frame, known_face_encodings, file_path)
    cv2.imshow("Frame", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    k = cv2.waitKey(1)

cv2.destroyAllWindows()
