
import os
import cv2
import pygame
import pygame.camera
import face_recognition
import RPi.GPIO as gpio

gpio.setmode (gpio.BCM)
gpio.setwarnings (False)
gpio.setup (21, gpio.IN, pull_up_down = gpio.PUD_UP)

path = "RealTimeImages/EncodingImages"
image_type = "Image"
image_counter = len([i for i in os.listdir(path) if image_type in i])

flag = 0

file = open (os.path.abspath ("RealTimeImages/names.txt"), "a+")

pygame.camera.init ()
lst = pygame.camera.list_cameras()

cam = pygame.camera.Camera (lst[0], (640, 480))
cam.start()

while flag == 0:
	frame = pygame.surfarray.array3d(cam.get_image()).swapaxes(0, 1)
	cv2.imshow("Capturing Images....", cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY))
	k = cv2.waitKey (1)
	
	input_state = gpio.input (21)
	
	if input_state == 0 :
		encodings = face_recognition.face_encodings (frame)

		if len(encodings) == 1 :

			print ("Enter the Name of the person")
			name = input ()

			image_name = "Image{}.jpg".format(image_counter)
			path = path + "/" + image_name
			
			cv2.imwrite(os.path.abspath (path), frame)
			print("{} written!".format(image_name))
			
			image_counter += 1
			flag = 1

			file.write (name + "\n")

		elif len (encodings) == 0 :
			print ("Cannot find a Face in the image")

			if k % 256 == 27 :
				print ("Capturing the image again")
		else :
			print ("More than 1 Faces are in front of the screen")

			if k % 256 == 27 :
				print ("Capturing the image again")

file.close ()

cv2.destroyAllWindows()
