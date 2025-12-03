import cv2
import time
import pyautogui
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

SCROLL_SPEED = 300
SCROLL_DELAY = 1

CAM_WIDTH, CAM_HEIGHT = 640, 450

def detect_gesture(landmarks, handedness):
    fingers = []
    tips = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]

    for tip in tips:
        if landmarks.landmark[tip].y < landmarks.landmark[tip - 2].y:
            fingers.append(1)

    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]

    if (handedness == 'Right' and thumb_tip.x > thumb_ip.x) or \
       (handedness == 'Left' and thumb_tip.x < thumb_ip.x):
        fingers.append(1)

    return "scroll_up" if sum(fingers) == 5 else "scroll_down" if len(fingers) == 0 else "none"

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, CAM_WIDTH)
    cap.set(4, CAM_HEIGHT)

    last_scroll = 0
    p_time = 0

    print("Gesture Scroll Active\nOpen palm: Scroll Up\nClosed fist: Scroll Down\nPress 'q' to Exit")

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(img_rgb)
        gesture, handedness = "none", "Unknown"

        if results.multi_hand_landmarks:
            for hand, handedness_info in zip(results.multi_hand_landmarks, results.multi_handedness):
                handedness = handedness_info.classification[0].label
                gesture = detect_gesture(hand, handedness)

                mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

                if gesture == "scroll_up" and time.time() - last_scroll > SCROLL_DELAY:
                    pyautogui.scroll(SCROLL_SPEED)
                    last_scroll = time.time()
                elif gesture == "scroll_down" and time.time() - last_scroll > SCROLL_DELAY:
                    pyautogui.scroll(-SCROLL_SPEED)
                    last_scroll = time.time()

        fps = 1 / (time.time() - p_time) if (time.time() - p_time) > 0 else 0
        p_time = time.time()

        cv2.putText(img, f'FPS: {int(fps)}', (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(img, f'Gesture: {gesture}', (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("Gesture Scroll", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()