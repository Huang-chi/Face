import face_recognition
from os import listdir
from os.path import isfile, isdir, join



def load_all_image(files,file_path):
	print ("Loading The Known Images....")
	known_encodings = []
	known_names = []
	for file in files:
		image = face_recognition.load_image_file (join(file_path,file))

		known_encoding = face_recognition.face_encodings (image)
		
		known_encodings.append (known_encoding[0])
		known_names.append(file)

	return known_encodings, known_names
