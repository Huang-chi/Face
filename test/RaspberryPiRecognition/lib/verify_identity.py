import face_recognition
import cv2

def verify_image(files,gray,id,test_face_locations):
	for i, test_face_location in zip (id, test_face_locations) :
		(top, right, bottom, left) = test_face_location

		cv2.rectangle (gray, (left - 10, top - 40), (right + 10, bottom), (0, 205, 0), 2)

		font = cv2.FONT_HERSHEY_SIMPLEX
		print("--")
		print(i)
		if i[0] == -1 :
				cv2.putText(gray, "ID : Unknown", ((left + right) // 2 - 25, bottom + 15), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
				print ("The person is not in the database")
		else :
				cv2.putText(gray, "ID : " + str (files [i[0]][:-3]), ((left + right) // 2 - 25, bottom + 15), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
				print ("Welcome " + files[i[0]][:-4])
		return gray, files[i[0]][:-4]

def compare_image(known_face_encodings, encodings):
	flag2 = 0
	for encoding in encodings :
		matches = face_recognition.compare_faces (known_face_encodings, encoding,0.5)
		if True in matches :
			print ("The Person is already saved in the database")
			flag2 = 1
			
	return flag2

def verify_face_is_in_system(test_face_encodings,known_encodings,id):
	open = 0
	for test_face_encoding in test_face_encodings :
		matches = face_recognition.compare_faces (known_encodings, test_face_encoding,0.5)
		if True in matches :
			id.append ([i for i in range (len(matches)) if matches[i]])
			open = 1
		else :
			id.append ([-1])
	print(id)
			
	return open, id
