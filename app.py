import cv2
import face_recognition
import numpy as np
import pandas as pd
import os
import datetime
import tkinter as tk
from tkinter import Label, Entry, Button, messagebox
from PIL import Image, ImageTk

# Paths for dataset storage
KNOWN_FACES_DIR = "known_faces"
ATTENDANCE_FILE = "attendance.xlsx"
USERS_FILE = "users.csv"

# Ensure directories exist
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

# Load registered faces
def load_known_faces():
    known_face_encodings = []
    known_face_names = []

    if os.path.exists(USERS_FILE):
        users_df = pd.read_csv(USERS_FILE)
        for _, row in users_df.iterrows():
            file_name = f"{KNOWN_FACES_DIR}/{row['ID']}_{row['Name']}.jpg"
            if os.path.exists(file_name):
                image = face_recognition.load_image_file(file_name)
                encoding = face_recognition.face_encodings(image)
                if encoding:
                    known_face_encodings.append(encoding[0])
                    known_face_names.append(f"{row['ID']} - {row['Name']}")

    return known_face_encodings, known_face_names

known_face_encodings, known_face_names = load_known_faces()

# Mark attendance only once per hour
def mark_attendance(name, person_id):
    now = datetime.datetime.now()
    current_hour = now.replace(minute=0, second=0, microsecond=0)

    if os.path.exists(ATTENDANCE_FILE):
        attendance_df = pd.read_excel(ATTENDANCE_FILE)
        attendance_df['Time'] = pd.to_datetime(attendance_df['Time'])

        recent_entries = attendance_df[
            (attendance_df['ID'] == person_id) &
            (attendance_df['Time'] >= current_hour)
        ]

        if not recent_entries.empty:
            return

        new_entry = pd.DataFrame([[person_id, name, now.strftime("%Y-%m-%d %H:%M:%S")]], columns=["ID", "Name", "Time"])
        attendance_df = pd.concat([attendance_df, new_entry], ignore_index=True)
        attendance_df.to_excel(ATTENDANCE_FILE, index=False)

    else:
        new_entry = pd.DataFrame([[person_id, name, now.strftime("%Y-%m-%d %H:%M:%S")]], columns=["ID", "Name", "Time"])
        new_entry.to_excel(ATTENDANCE_FILE, index=False)

# Tkinter UI Setup
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.attributes('-fullscreen', True)

# Header
header = tk.Frame(root, bg="black", height=60)
header.pack(fill="x")

header_label = tk.Label(header, text="Face Recognition Attendance System", fg="white", bg="black", font=("Sans", 24, "bold"))
header_label.pack(pady=10)

# Body Frame
body_frame = tk.Frame(root, bg="white")
body_frame.pack(expand=True, fill="both")

# Fixed camera size
camera_frame = tk.Frame(body_frame, bg="white")
camera_frame.place(relx=0.5, rely=0.4, anchor="center")

video_label = Label(camera_frame, bg="black", width=640, height=480)
video_label.pack()

# Details Frame
details_frame = tk.Frame(body_frame, bg="white")
details_frame.place(relx=0.5, rely=0.85, anchor="center")

name_label = Label(details_frame, text="Name: -", font=("Sans", 16), bg="white")
name_label.grid(row=0, column=0, padx=20, pady=5)

id_label = Label(details_frame, text="ID: -", font=("Sans", 16), bg="white")
id_label.grid(row=0, column=1, padx=20, pady=5)

time_label = Label(details_frame, text="Timestamp: -", font=("Sans", 16), bg="white")
time_label.grid(row=0, column=2, padx=20, pady=5)

# Buttons
exit_button = Button(root, text="Exit", command=root.quit, font=("Sans", 16), bg="black", fg="white", width=10)
exit_button.place(relx=0.02, rely=0.95, anchor="sw")

register_button = Button(root, text="Register New Face", font=("Sans", 16), bg="black", fg="white", width=15)
register_button.place(relx=0.98, rely=0.95, anchor="se")

# Start Video Capture
cap = cv2.VideoCapture(0)

def update_frame():
    ret, frame = cap.read()
    if not ret:
        return

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.5, fy=0.5)
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    detected_name = "Unknown"
    detected_id = "-"
    detected_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances) if len(face_distances) > 0 else None

        if best_match_index is not None and matches[best_match_index]:
            detected_name = known_face_names[best_match_index].split(" - ")[1]
            detected_id = known_face_names[best_match_index].split(" - ")[0]
            mark_attendance(detected_name, detected_id)

    name_label.config(text=f"Name: {detected_name}")
    id_label.config(text=f"ID: {detected_id}")
    time_label.config(text=f"Timestamp: {detected_time}")

    img = Image.fromarray(rgb_frame)
    img = img.resize((640, 480))
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    root.after(10, update_frame)

# Register New User Function
def register_user():
    register_window = tk.Toplevel(root)
    register_window.title("Register New User")
    register_window.geometry("400x300")

    tk.Label(register_window, text="Enter ID:", font=("Sans", 12)).pack(pady=5)
    id_entry = Entry(register_window, font=("Sans", 12))
    id_entry.pack(pady=5)

    tk.Label(register_window, text="Enter Name:", font=("Sans", 12)).pack(pady=5)
    name_entry = Entry(register_window, font=("Sans", 12))
    name_entry.pack(pady=5)

    def capture_face():
        user_id = id_entry.get().strip()
        user_name = name_entry.get().strip()

        if not user_id or not user_name:
            messagebox.showerror("Error", "Please enter ID and Name!")
            return

        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture image!")
            return

        file_path = f"{KNOWN_FACES_DIR}/{user_id}_{user_name}.jpg"
        cv2.imwrite(file_path, frame)

        new_user = pd.DataFrame([[user_id, user_name]], columns=["ID", "Name"])
        if os.path.exists(USERS_FILE):
            new_user.to_csv(USERS_FILE, mode='a', header=False, index=False)
        else:
            new_user.to_csv(USERS_FILE, index=False)

        global known_face_encodings, known_face_names
        known_face_encodings, known_face_names = load_known_faces()

        messagebox.showinfo("Success", "User registered successfully!")
        register_window.destroy()

    tk.Button(register_window, text="Capture & Register", command=capture_face, font=("Sans", 12), bg="black", fg="white").pack(pady=20)

register_button.config(command=register_user)

# Start video feed
update_frame()

# Run the Tkinter app
root.mainloop()

# Release camera
cap.release()
cv2.destroyAllWindows()
