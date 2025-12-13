# Real-Time Face Tracking & People Count + Image Manipulation
# Requirements: pip install opencv-python
# Download Haarcascade if missing: cv2.data.haarcascades provides path

import cv2
import numpy as np

def adjust_brightness(img, value):
    # value: -100 to 100
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = np.clip(v.astype(np.int16) + value, 0, 255).astype(np.uint8)
    hsv = cv2.merge((h, s, v))
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def rotate_image(img, angle):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
    return cv2.warpAffine(img, M, (w, h))

def crop_center(img, percent=0.7):
    h, w = img.shape[:2]
    ch, cw = int(h * percent), int(w * percent)
    y0 = (h - ch) // 2
    x0 = (w - cw) // 2
    return img[y0:y0+ch, x0:x0+cw]

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    angle = 0
    brightness = 0
    crop_p = 1.0

    info = "Keys: a/d rotate, j/k brightness -, +, c crop toggle, r reset, q/ESC quit"

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)

        # Manipulations in order: rotate, brightness, crop (for display)
        manipulated = rotate_image(frame, angle)
        manipulated = adjust_brightness(manipulated, brightness)
        display = manipulated.copy()
        if crop_p < 1.0:
            display = crop_center(display, crop_p)

        gray = cv2.cvtColor(display, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 6)

        # Draw faces and count
        for (x, y, w, h) in faces:
            cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(display, f"People count (faces): {len(faces)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display, info, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(display, f"Angle: {angle} | Brightness: {brightness} | Crop: {crop_p:.2f}",
                    (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

        cv2.imshow("Face Tracking & People Count + Manipulation", display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('a'):
            angle -= 5
        elif key == ord('d'):
            angle += 5
        elif key == ord('j'):
            brightness = max(brightness - 5, -100)
        elif key == ord('k'):
            brightness = min(brightness + 5, 100)
        elif key == ord('c'):
            crop_p = 0.7 if crop_p == 1.0 else 1.0
        elif key == ord('r'):
            angle, brightness, crop_p = 0, 0, 1.0
        elif key == 27 or key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
