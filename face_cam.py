import cv2
from PIL import Image, ImageTk
import PIL.Image
import face_recognition
import mysql.connector
import os
import numpy as np
from datetime import datetime

def face_camera(tablename):
    if not os.path.exists('db'):
        os.makedirs('db')
    # Load all images in the "db" folder and learn how to recognize them.
    known_face_encodings = []
    known_face_names = []
    for filename in os.listdir("db"):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image = face_recognition.load_image_file("db\\" + filename)
            face_encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(os.path.splitext(filename)[0])

    video_capture = cv2.VideoCapture(0)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                if name != "Unknown" or "":
                    face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Check if the current face matches any of the images in the db folder
            for filename in os.listdir("db"):
                if not filename.endswith(".jpg"):
                    continue
                filepath = os.path.join("db", filename)
                image = face_recognition.load_image_file(filepath)
                encoding = face_recognition.face_encodings(image)[0]
                distance = face_recognition.face_distance([encoding], face_encoding)[0]
                if distance < 0.6:
                    name = filename[:-4]  # Remove the ".jpg" extension
                    cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (0, 255, 0), 1)

                    # Establish a connection to the database
                    db = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="Shubham@123",
                        database="attendance"
                    )

                    # Create a cursor object
                    cursor = db.cursor()

                    # Define the table name and column names
                    table_name = tablename

                    # Define the query with parameter placeholders (%s)
                    query = "INSERT INTO {} (name, date, time) VALUES (%s, %s, %s)".format(table_name)

                    # Define the variable values to be inserted
                    now = datetime.now()
                    name = known_face_names[best_match_index]

                    # Extract the date and time components
                    date = now.date()
                    time = now.time()

                    # Execute the query with the variable values as parameters
                    cursor.execute(query, (name, date, time))

                    # Commit the changes to the database
                    db.commit()

                    # Close the cursor and database connection
                    cursor.close()
                    db.close()

                    break

        # Display the resulting image
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()