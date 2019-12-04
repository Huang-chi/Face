import face_recognition
import cv2

video_capture = cv2.VideoCapture(0)

# Load a second sample picture and learn how to recognize it.
Steven_image = face_recognition.load_image_file("Steven.png")
Steven_face_encoding = face_recognition.face_encodings(Steven_image)[0]

Robert_image = face_recognition.load_image_file("Robert.jpg")
Robert_face_encoding = face_recognition.face_encodings(Robert_image)[0]

Janet_image = face_recognition.load_image_file("Janet.jpg")
Janet_face_encoding = face_recognition.face_encodings(Janet_image)[0]

red_image = face_recognition.load_image_file("red.jpg")
red_face_encoding = face_recognition.face_encodings(red_image)[0]

Carol_image = face_recognition.load_image_file("Carol.jpg")
Carol_face_encoding = face_recognition.face_encodings(Carol_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    Steven_face_encoding,
    Robert_face_encoding,
    Janet_face_encoding,
    red_face_encoding,
    Carol_face_encoding
]

known_face_names = [
    "Steven",
    "Robert",
    "Janet",
    "red",
    "Carol"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video

        # Returns an array of bounding boxes of human faces in a image
        face_locations = face_recognition.face_locations(rgb_small_frame)

        # Returns a list of 128-dimensional face encodings (one for each face in the image)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations) # The second parameter is optional, means a bounding boxesof each face that we already know where it locates

        face_names = []

        for face_encoding in face_encodings:

            # See if the face is a match for the known face(s)

            # face_recognition.compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6)
            #    1. known_face_encodings -> A list of known face encodings
            #    2. face_encoding_to_check -> A single face encoding to compare against the list
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.45)
            
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                # Return True value's index in match list
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

#    process_this_frame = not process_this_frame


    # Display the results
    # zip: https://github.com/KBLin1996/Python_Practice/edit/master/basic_python.py 
    for(top, right, bottom, left), name in zip(face_locations, face_names):

        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        # 在這裡改顏色 -> if OK (green), else if Maybe (yellow), else Unknown (red)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        # cv2.rectangle(frame, vertex's coordinate, diagonal's coordinate, line color, line breadth)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

        # cv2.putText(frame, test, coordinate, font, size, text color, text breadth, line options (optional))
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Face Recognition', frame)

    # Hit 'q' on the keyboard to quit !
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
