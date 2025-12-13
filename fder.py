# Real-Time Face Detection + Emotion Recognition
# Requirements:
# - pip install opencv-python
# - Option A (easiest): pip install fer  (uses a pretrained emotion model)
#   If FER isn't available, the script will still run face detection and show "Unknown" emotion.

import cv2
import numpy as np

# Try to import FER
HAS_FER = False
try:
    from fer import FER
    HAS_FER = True
except Exception:
    HAS_FER = False

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    detector = FER() if HAS_FER else None

    info = "Press q/ESC to quit"

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(60, 60))

        for (x, y, w, h) in faces:
            roi = frame[y:y+h, x:x+w].copy()

            emotion_label = "Unknown"
            confidence = 0.0

            if detector is not None:
                try:
                    result = detector.top_emotion(roi)
                    if result is not None:
                        emotion_label, confidence = result
                except Exception:
                    pass

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{emotion_label} ({int(confidence * 100)}%)", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.putText(frame, info, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Face Detection + Emotion Recognition", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
