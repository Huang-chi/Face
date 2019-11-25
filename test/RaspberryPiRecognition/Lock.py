import face_recognition
import RPi.GPIO as gpio
import pygame
import pygame.camera
import time
import os
import cv2

gpio.setmode (gpio.BCM)
gpio.setwarnings (False)
gpio.setup (21, gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.setup (16, gpio.OUT)

gpio.output (16, gpio.LOW)

file = open (os.path.abspath ("RealTimeImages/names.txt"), "r")

known_encodings = []
known_names = file.readlines()

path = "RealTimeImages/EncodingImages"
image_type = "Image"
counter = len([i for i in os.listdir(path) if image_type in i])
print (counter)

print ("Loading The Known Images....")
for i in range (counter) :
	path = "RealTimeImages/EncodingImages/Image" + str(i) + ".jpg"
	image = face_recognition.load_image_file (os.path.abspath(path))

	known_encoding = face_recognition.face_encodings (image)
	known_encodings.append (known_encoding[0])

pygame.camera.init()
lst = pygame.camera.list_cameras()

cam = pygame.camera.Camera (lst[0], (640, 480))
cam.start()

while True :
	test_image = pygame.surfarray.array3d (cam.get_image()).swapaxes (0, 1)
	input_state = gpio.input (21)
	
	id = []
	open = 0
	gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
	
	if input_state == 0 :
		test_face_encodings = face_recognition.face_encodings (test_image)
		test_face_locations = face_recognition.face_locations (test_image)
		
		for test_face_encoding in test_face_encodings :
			matches = face_recognition.compare_faces (known_encodings, test_face_encoding)
			
			if True in matches :
				id.append ([i for i in range (len(matches)) if matches[i]])
				open = 1
			else :
				id.append ([-1])
			
		for i, test_face_location in zip (id, test_face_locations) :
			(top, right, bottom, left) = test_face_location
			 
			cv2.rectangle (gray, (left - 10, top - 40), (right + 10, bottom), (0, 205, 0), 2)
			
			font = cv2.FONT_HERSHEY_SIMPLEX
			if i[0] == -1 :
				cv2.putText(gray, "ID : Unknown", ((left + right) // 2 - 25, bottom + 15), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
				print ("The person is not in the database")
			else :
				cv2.putText(gray, "ID : " + str (known_names [i[0]][:-1]), ((left + right) // 2 - 25, bottom + 15), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
				print ("Welcome " + known_names[i[0]][:-1])
		cv2.destroyWindow ("Frame")
		cv2.imshow ("Frame", gray)
		k = cv2.waitKey (1)
		
		if open == 1 :
			gpio.output (16, gpio.HIGH)
			time.sleep (5)
			gpio.output (16, gpio.LOW)
	
	cv2.imshow ("Frame", cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY))
	k = cv2.waitKey (1)
gpio.cleanup()
