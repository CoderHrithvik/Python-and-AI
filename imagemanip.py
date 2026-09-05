import cv2
import numpy as np

# Load OpenCV's built‑in face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Start webcam
cap = cv2.VideoCapture(0)

# Image manipulation settings
rotation_angle = 0
brightness_value = 0
crop_enabled = False

print("Controls:")
print("  R = Rotate image")
print("  B = Increase brightness")
print("  N = Decrease brightness")
print("  C = Toggle crop mode")
print("  Q = Quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # -------------------- Brightness Adjustment --------------------
    frame = cv2.convertScaleAbs(frame, alpha=1, beta=brightness_value)

    # -------------------- Rotation --------------------
    if rotation_angle != 0:
        h, w = frame.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
        frame = cv2.warpAffine(frame, matrix, (w, h))

    # -------------------- Cropping --------------------
    if crop_enabled:
        h, w = frame.shape[:2]
        frame = frame[h//4 : 3*h//4, w//4 : 3*w//4]

    # -------------------- Face Detection --------------------
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 6)

    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # People count
    count = len(faces)
    cv2.putText(frame, f"People Count: {count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    # Show frame
    cv2.imshow("Face Tracking & Image Manipulation", frame)

    # -------------------- Keyboard Controls --------------------
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('r'):
        rotation_angle = (rotation_angle + 90) % 360
    elif key == ord('b'):
        brightness_value = min(brightness_value + 10, 100)
    elif key == ord('n'):
        brightness_value = max(brightness_value - 10, -100)
    elif key == ord('c'):
        crop_enabled = not crop_enabled

cap.release()
cv2.destroyAllWindows()