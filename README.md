# Facial Recognition Attendance System

### Problem Statement:
Developing a facial recognition attendance system that accurately identifies individuals in real-time under various conditions and gives analytics about the attendance

### Technologies Used:
- Face Recognition is used to recgonize face and the facial features and then match it with the database
- Tkinter is used for GUI
- cv2 is used to get the image for registering user
- Sql is used to store the data

### Methodology:
The methodology involves using the face_recognition library to match facial features from the collected data with a database of known faces. The data is stored in an SQL database, which includes attendance data, login IDs, and passwords while the face data is stored on a folder locally. A graphical user interface is created using tkinter to present the workflow and capture a photo of the user while registering, which is processed using the cv2 library. Attendance data is analyzed using numpy and pandas to generate reports or insights.

Overall, the methodology involves the following steps:

- Collect facial image dataset and store it in an SQL database
- Use the face_recognition library to match facial features from the collected data with a database of known faces
- Store the matched face data, attendance data, login IDs, and passwords in an SQL database
- Create a graphical user interface using tkinter to present the workflow and capture a photo of the user while registering, which is processed using the cv2 library
- Analyze attendance data using numpy and pandas to generate reports or insights.

### Working steps:
- Student should login or register into the portal while teacher would be given a common id and password to access the admin dashboard
- Students are supposed to scan their faces while registering 
- The teacher would have different dashboard and student would have different dashboard
- Student dashboard contains the students academic attedance of the month
- Tecahers dashboard consists of two major things, firstly there will be an option to coduct students attendance where teacher has to select the department first and then the subject and then scan the students face to register their attendance. The next option is Teachers Profile which contains the academic attendance of students department wise

### Work flow:
![image](https://user-images.githubusercontent.com/102586176/234610296-133dcbc9-13ae-4f95-9d87-5d7d6655b598.png)


### Challenges:
- The face recognition library needs dlib and CMake, which are C++ libraries. It was a big task installing them, and a [YouTube tutorial](https://youtu.be/eaEndTeUiSU) helped me do it.
- We need Visual Code Studio for C++ web development to make dlib and cmake work.
- Also, the integration of Tkinter with OpenCV was a task that took a lot of research and work.

### Demo
Youtube video of working: https://youtu.be/E455BzxC8hE
