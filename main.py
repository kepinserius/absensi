import cv2
import pandas as pd
import os
from datetime import datetime

def mark_attendance(name):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists("absensi.csv"):
        df = pd.DataFrame(columns=["Name", "Timestamp"])
        df.to_csv("absensi.csv", index=False)

    df = pd.read_csv("absensi.csv")
    if not ((df["Name"] == name) & (df["Timestamp"].str.contains(now.strftime("%Y-%m-%d")))).any():
        df = df.append({"Name": name, "Timestamp": timestamp}, ignore_index=True)
        df.to_csv("absensi.csv", index=False)
        print(f"Absensi berhasil untuk {name} pada {timestamp}")

def recognize_face():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("recognizer/face_model.yml")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    people = os.listdir("dataset/")

    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            label, confidence = recognizer.predict(face)
            if confidence < 50:  # Ambang batas akurasi
                name = people[label]
                mark_attendance(name)
                cv2.putText(frame, f"{name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            else:
                cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow("Absensi Wajah", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Tekan 'q' untuk keluar
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_face()
