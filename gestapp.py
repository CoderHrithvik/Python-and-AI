import cv2
import mediapipe as mp
import time
import numpy as np

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

FILTERS = ["none", "gray", "sepia", "negative", "blur"]

def apply_filter(frame, filter_name):
    if filter_name == "gray":
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if filter_name == "sepia":
        kernel = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        sepia_filter = cv2.transform(kernel, 
            np.array([[0.272, 0.534, 0.131],
                      [0.349, 0.686, 0.168],
                      [0.393, 0.769, 0.189]])
                      
                    )
        return cv2.cvtColor(sepia_filter, cv2.COLOR_RGB2BGR)
    if filter_name == "negative":
        return cv2.bitwise_not(frame)
    if filter_name == "blur":
        return cv2.GaussianBlur(frame, (15, 15), 0)
    return frame

def main():
    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands(min_detection_confidence=0.7,
                           min_tracking_confidence=0.7)
    current_filter_idx = 0
    last_capture_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        h, w, _ = frame.shape
        thumb_tip = None
        index_tip = None
        other_tips = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks,
                                       mp_hands.HAND_CONNECTIONS)
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]
                for tip_id in [12, 16, 20]:
                    other_tips.append(hand_landmarks.landmark[tip_id])

        # Gesture logic
        if thumb_tip and index_tip:
            # Distance between thumb and index
            dx = (thumb_tip.x - index_tip.x) * w
            dy = (thumb_tip.y - index_tip.y) * h
            dist = (dx**2 + dy**2) ** 0.5

            # Thumb touching index -> capture
            if dist < 40 and time.time() - last_capture_time > 1:
                last_capture_time = time.time()
                filename = f"capture_{int(time.time())}.png"
                cv2.imwrite(filename, frame)
                cv2.putText(frame, f"Captured: {filename}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Thumb close to any other finger tip -> change filter
            for tip in other_tips:
                dx2 = (thumb_tip.x - tip.x) * w
                dy2 = (thumb_tip.y - tip.y) * h
                dist2 = (dx2**2 + dy2**2) ** 0.5
                if dist2 < 40 and time.time() - last_capture_time > 0.5:
                    last_capture_time = time.time()
                    current_filter_idx = (current_filter_idx + 1) % len(FILTERS)

        filter_name = FILTERS[current_filter_idx]
        display_frame = apply_filter(frame.copy(), filter_name)
        if filter_name == "gray":
            display_frame = cv2.cvtColor(display_frame, cv2.COLOR_GRAY2BGR)

        cv2.putText(display_frame, f"Filter: {filter_name}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        cv2.imshow("Gesture Photo App", display_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()