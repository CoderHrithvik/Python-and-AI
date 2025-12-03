import cv2
import mediapipe as mp
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

# ------------------ Setup Volume Control (PyCaw) ------------------
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()  # (min, max, step)
min_vol, max_vol = vol_range[0], vol_range[1]

# ------------------ Setup Mediapipe ------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)  # detect both hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms, handType in zip(results.multi_hand_landmarks, results.multi_handedness):
            # Thumb tip = 4, Index tip = 8
            thumb = handLms.landmark[4]
            index = handLms.landmark[8]

            h, w, c = img.shape
            x1, y1 = int(thumb.x * w), int(thumb.y * h)
            x2, y2 = int(index.x * w), int(index.y * h)

            cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

            # Distance between thumb and index
            length = np.hypot(x2 - x1, y2 - y1)

            # Check if it's left or right hand
            label = handType.classification[0].label  # 'Left' or 'Right'

            if label == "Right":
                # Map distance to volume
                vol = np.interp(length, [20, 200], [min_vol, max_vol])
                volume.SetMasterVolumeLevel(vol, None)
                vol_percent = int(np.interp(length, [20, 200], [0, 100]))

                # Progress bar for volume
                cv2.rectangle(img, (50, 150), (85, 400), (255, 255, 255), 3)
                cv2.rectangle(img, (50, int(400 - (vol_percent * 2.5))), (85, 400), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'Vol: {vol_percent}%', (40, 430),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            elif label == "Left":
                # Map distance to brightness
                brightness = np.interp(length, [20, 200], [0, 100])
                sbc.set_brightness(int(brightness))

                # Progress bar for brightness
                cv2.rectangle(img, (150, 150), (185, 400), (255, 255, 255), 3)
                cv2.rectangle(img, (150, int(400 - (brightness * 2.5))), (185, 400), (0, 255, 255), cv2.FILLED)
                cv2.putText(img, f'Bright: {int(brightness)}%', (130, 430),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            # Draw landmarks
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
