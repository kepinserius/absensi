import cv2
import os

# Fungsi untuk menambahkan data wajah
def add_face(nama):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cam = cv2.VideoCapture(0)

    print(f"Menambahkan data wajah untuk: {nama}")
    count = 0
    folder_path = f"dataset/{nama}"
    os.makedirs(folder_path, exist_ok=True)

    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            count += 1
            face = gray[y:y + h, x:x + w]
            file_name = f"{folder_path}/{count}.jpg"
            cv2.imwrite(file_name, face)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow("Menambahkan Wajah", frame)

        if count >= 30 or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    print(f"Data wajah untuk {nama} berhasil ditambahkan!")

if __name__ == "__main__":
    name = input("Masukkan nama orang: ")
    add_face(name)
