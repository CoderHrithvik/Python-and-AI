import cv2
import mediapipe as mp
import os
import time

def apply_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def apply_sepia(img):
    kernel = cv2.transform(np.array([[0.272, 0.534, 0.131],
                                     [0.349, 0.686, 0.168],
                                     [0.393, 0.769, 0.189]], dtype="float32"))
    return cv2.transform(img, kernel)

def apply_negative(img):
    return 255 - img

def apply_blur(img, ksize=15):
    return cv2.GaussianBlur(img, (ksize, ksize), 0)

import numpy as np

FILTERS = ["none", "grayscale", "sepia", "negative", "blur"]

def apply_filter(img, name):
    if name == "none":
        return img
    if name == "grayscale":
        g = apply_grayscale(img)
        return cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)
    if name == "sepia":
        out = apply_sepia(img)
        return np.clip(out, 0, 255).astype(np.uint8)
    if name == "negative":
        return apply_negative(img)
    if name == "blur":
        return apply_blur(img)
    return img

def draw_text(frame, text, y=30, color=(255, 255, 255)):
    cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def is_thumb_touching(finger_tip_idx, landmarks, w, h, thresh=0.05):

    thumb = landmarks[4]
    finger = landmarks[finger_tip_idx]
    tx, ty = thumb.x * w, thumb.y * h
    fx, fy = finger.x * w, finger.y * h
    dist = np.hypot(tx - fx, ty - fy)
    diag = np.hypot(w, h)
    return dist / diag < thresh

def next_filter(current):
    idx = FILTERS.index(current)
    return FILTERS[(idx + 1) % len(FILTERS)]

def prev_filter(current):
    idx = FILTERS.index(current)
    return FILTERS[(idx - 1) % len(FILTERS)]

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    os.makedirs("output", exist_ok=True)
    current_filter = "none"
    last_capture_time = 0
    debounce_capture_sec = 0.8
    debounce_filter_sec = 0.4
    last_filter_change = 0

    with mp_hands.Hands(
        model_complexity=1,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            gesture_info = "Gesture: "
            if result.multi_hand_landmarks:
                landmarks = result.multi_hand_landmarks[0].landmark

                mp_drawing.draw_landmarks(
                    frame, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS
                )

                now = time.time()
                if is_thumb_touching(8, landmarks, w, h):  
                    gesture_info += "Capture"
                    if now - last_capture_time > debounce_capture_sec:
                        filtered = apply_filter(frame.copy(), current_filter)
                        filename = f"output/capture_{int(now)}_{current_filter}.png"
                        cv2.imwrite(filename, filtered)
                        last_capture_time = now
                        draw_text(frame, f"Captured: {os.path.basename(filename)}", y=60, color=(0, 255, 0))
                elif is_thumb_touching(12, landmarks, w, h):  
                    gesture_info += "Next filter"
                    if now - last_filter_change > debounce_filter_sec:
                        current_filter = next_filter(current_filter)
                        last_filter_change = now
                elif is_thumb_touching(16, landmarks, w, h):  
                    gesture_info += "Prev filter"
                    if now - last_filter_change > debounce_filter_sec:
                        current_filter = prev_filter(current_filter)
                        last_filter_change = now
                elif is_thumb_touching(20, landmarks, w, h):  
                    gesture_info += "Reset filter"
                    if now - last_filter_change > debounce_filter_sec:
                        current_filter = "none"
                        last_filter_change = now
                else:
                    gesture_info += "None"

            preview = apply_filter(frame.copy(), current_filter)

            draw_text(preview, f"Filter: {current_filter}", y=30)
            draw_text(preview, gesture_info, y=60)

            cv2.imshow("Gesture Photo App (Thumb-Finger)", preview)
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
