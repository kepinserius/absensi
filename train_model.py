import cv2
import os
import numpy as np

def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    faces, labels = [], []
    people = os.listdir("dataset/")

    for label, person in enumerate(people):
        folder_path = f"dataset/{person}"
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            faces.append(image)
            labels.append(label)

    recognizer.train(faces, np.array(labels))
    recognizer.save("recognizer/face_model.yml")
    print("Model berhasil dilatih!")

if __name__ == "__main__":
    train_model()
