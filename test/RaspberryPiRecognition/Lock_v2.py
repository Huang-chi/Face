import face_recognition
import RPi.GPIO as gpio
import pygame
import pygame.camera
import time
import os
import cv2
from os import listdir
from os.path import isfile, isdir, join
from threading import Thread

###
from lib.verify_identity import verify_image
from lib.verify_identity import verify_face_is_in_system
from lib.load import load_all_image
from lib.verify_identity import compare_image
###

openface_or_dlib = 1 #openface = 0 or dlib = 1

def Lock(image_array, known_encodings, names):
        #op = main()        
        
        open = [0,0,0]
        
        
        
        for i in range(0,3):
                id = []
                test_image = image_array[i]
                gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
                
                start = float(time.time())
                
                test_face_encodings = face_recognition.face_encodings (test_image)
                

                flag2 = compare_image(known_encodings, test_face_encodings)
                print(len(test_face_encodings),flag2)
                if len(test_face_encodings) == 1 and flag2 == 1:
                        test_face_locations = face_recognition.face_locations (test_image)
                
                        print(float(time.time()) - start)
                
                        open_temp, id = verify_face_is_in_system(test_face_encodings, known_encodings, id)
                        gray, name= verify_image(names,gray,id,test_face_locations)
                        open[i] = open_temp
                        print(open[i])
                        
                elif len (test_face_encodings) == 0 :
                        print ("Cannot find a Face in the image")
                else :
                        print ("More than 1 Faces are in front of the screen")
                        
        print("open")
        print(open)
        open[0] = open[0]+open[1]+open[2]
        
        cv2.destroyWindow ("Frame")
        cv2.imshow ("Frame", gray)
        k = cv2.waitKey (1)
        return open[0]
