# Face-Recognition-Attendence-System
# 🧠 Face Recognition Attendance System

This project is a real-time Face Recognition-based Attendance System built using **Python**, **OpenCV**, and **face_recognition** library. It identifies faces from webcam input and marks attendance with timestamps, ensuring each person is logged only once per hour. It features a stylish GUI built with Tkinter.


 🚀 Features

- 🎥 Real-time face detection via webcam
- 🔐 Face registration system with ID and Name
- 🧾 Logs attendance to an Excel sheet (`attendance.xlsx`)
- ⏱️ Automatically restricts duplicate entries within one hour
- 🎨 Responsive GUI with modern layout (camera in center, buttons at corners)
- 💾 Stores face encodings for future recognition
- ❌ Exit and ✅ Register buttons for control



🧰 Tech Stack

- **Python 3.8+**
- **OpenCV**
- **face_recognition**
- **Tkinter**
- **Pandas**
- **Pillow (PIL)**

---

📁 Project Structure
Face-Recognition-Attendence-System/


├── app.py # Main Python file

├── known_faces/ # Folder storing registered face images

├── users.csv # List of registered users (ID, Name)

├── attendance.xlsx # Excel file storing timestamped attendance

├── requirements.txt # List of dependencies

└── README.md # You're reading it!





**1. Install dependencies**
bash
pip install -r requirements.txt

**2. Run the app**
bash
python app.py



**How to Use**
➕ Register a New Face:
Click on Register button (bottom-right).

Enter ID and Name.

The system will capture a snapshot and save it under known_faces/.

**🧠 Mark Attendance:**
Run the app.

The camera detects and recognizes faces in real time.

Attendance is marked only once per hour per user in attendance.xlsx





**UI Design Highlights**
- Black header with title: "Face Recognition"

- Centered camera view in a rectangle box

- Names and timestamps listed below the frame

- Exit button at bottom-left

- Register button at bottom-right (white text, black background)

- Sans-serif font styling

- Fully responsive and fits all screen sizes


**Possible Improvements**
🔐 Add admin login for better security

☁️ Cloud integration (Firebase/GSheets)

📱 Mobile compatibility with Kivy or Flutter frontend

🎯 Improve face detection accuracy with deep learning models

**📄 License**
This project is licensed under the MIT License.






