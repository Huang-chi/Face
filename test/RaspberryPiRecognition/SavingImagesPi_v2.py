
import os
import cv2
import pygame
import pygame.camera
import face_recognition
from os import listdir
from os.path import isfile, isdir, join

####
from lib.load import load_all_image
from lib.verify_identity import compare_image
####


# path = "RealTimeImages/EncodingImages"
# image_type = "Image"
# image_counter = len([i for i in os.listdir(path) if image_type in i])

def SavingImages(frame, known_face_encodings, path):
	k = cv2.waitKey (1)
	image_type = "Image"
	image_counter = len([i for i in os.listdir(path) if image_type in i])

	encodings = face_recognition.face_encodings (frame)

	flag2 = compare_image(known_face_encodings, encodings)

	if len(encodings) == 1 and flag2 == 0:

		print ("Enter the Name of the person")
		name = input ()

		image_name = "Image_{}.jpg".format(name)
		path = path + "/" + image_name
			
		cv2.imwrite(os.path.abspath (path), cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
		print("{} written!".format(image_name))
		image_counter += 1
		flag = 1


	elif len (encodings) == 0 :
		print ("Cannot find a Face in the image")

		if k % 256 == 27 :
				print ("Capturing the image again")
	else :
		# print ("More than 1 Faces are in front of the screen")

		if k % 256 == 27 :
			print ("Capturing the image again")

