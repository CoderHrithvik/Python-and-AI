# Volume & Brightness Control Using Hand Gestures
# Requirements:
# - pip install opencv-python mediapipe
# - For Windows volume control: pip install pycaw
# - For brightness control: pip install screen-brightness-control
# Note: Volume control via Pycaw works on Windows. On macOS/Linux, brightness works; volume may need platform-specific libraries.

import cv2
import numpy as np
import mediapipe as mp
import platform
import time

# Optional modules with graceful fallback
HAS_PYCAW = False
HAS_BRIGHTNESS = False
try:
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from comtypes import CLSCTX_ALL
    import comtypes
    HAS_PYCAW = (platform.system() == "Windows")
except Exception:
    HAS_PYCAW = False

try:
    import screen_brightness_control as sbc
    HAS_BRIGHTNESS = True
except Exception:
    HAS_BRIGHTNESS = False

# Initialize volume interface (Windows)
def init_volume():
    if not HAS_PYCAW:
        return None
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = comtypes.client.CreateObject(interface)
        return volume
    except Exception:
        return None

# Map value utility
def map_value(x, in_min, in_max, out_min, out_max):
    x = np.clip(x, in_min, in_max)
    return out_min + (out_max - out_min) * (x - in_min) / (in_max - in_min)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    volume_interface = init_volume()
    vol_min, vol_max = -50.0, 0.0  # dB range typical for Pycaw
    brightness_min, brightness_max = 0, 100

    # Gesture distance bounds (pixels relative to diagonal)
    min_norm = 0.02
    max_norm = 0.20

    with mp_hands.Hands(
        max_num_hands=1,
        model_complexity=1,
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
            res = hands.process(rgb)

            volume_db = None
            brightness_val = None

            if res.multi_hand_landmarks:
                lm = res.multi_hand_landmarks[0].landmark
                mp_drawing.draw_landmarks(frame, res.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

                # Thumb tip (4), Index tip (8)
                t = lm[4]; i = lm[8]
                tx, ty = int(t.x * w), int(t.y * h)
                ix, iy = int(i.x * w), int(i.y * h)

                # Distance normalized to diagonal
                dist = np.hypot(tx - ix, ty - iy)
                diag = np.hypot(w, h)
                norm = dist / diag

                # Map to volume (dB) and brightness (%)
                mapped_vol = map_value(norm, min_norm, max_norm, vol_min, vol_max)
                mapped_bri = map_value(norm, min_norm, max_norm, brightness_min, brightness_max)

                # Apply volume
                if volume_interface is not None and HAS_PYCAW:
                    try:
                        volume_interface.SetMasterVolumeLevel(mapped_vol, None)
                        volume_db = mapped_vol
                    except Exception:
                        volume_db = None

                # Apply brightness
                if HAS_BRIGHTNESS:
                    try:
                        sbc.set_brightness(int(mapped_bri))
                        brightness_val = int(mapped_bri)
                    except Exception:
                        brightness_val = None

                # Visual feedback
                cv2.circle(frame, (tx, ty), 10, (0, 255, 0), -1)
                cv2.circle(frame, (ix, iy), 10, (0, 255, 0), -1)
                cv2.line(frame, (tx, ty), (ix, iy), (255, 255, 255), 2)

                # Bars
                # Volume bar (left)
                vol_display = map_value(norm, min_norm, max_norm, 0, 1)
                bri_display = map_value(norm, min_norm, max_norm, 0, 1)
                vol_bar_h = int(300 * vol_display)
                bri_bar_h = int(300 * bri_display)

                cv2.rectangle(frame, (30, 50), (60, 350), (100, 100, 100), 2)
                cv2.rectangle(frame, (32, 350 - vol_bar_h), (58, 348), (0, 255, 0), -1)
                cv2.putText(frame, f"VOL", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                if volume_db is not None:
                    cv2.putText(frame, f"{int(map_value(volume_db, vol_min, vol_max, 0, 100))}%", (20, 370),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # Brightness bar (right)
                cv2.rectangle(frame, (w - 60, 50), (w - 30, 350), (100, 100, 100), 2)
                cv2.rectangle(frame, (w - 58, 350 - bri_bar_h), (w - 32, 348), (0, 255, 255), -1)
                cv2.putText(frame, f"BRI", (w - 70, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                if brightness_val is not None:
                    cv2.putText(frame, f"{brightness_val}%", (w - 85, 370),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            cv2.imshow("Gesture Volume & Brightness", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
