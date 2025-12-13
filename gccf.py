# Gesture Control Basics with Color Filtering and Contours
# Idea: Track a colored object (e.g., blue glove or marker) and move/draw shapes based on centroid.
# Requirements: pip install opencv-python

import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    draw_mode = False
    path_points = []

    # HSV range for blue (adjust to your object color)
    lower = np.array([90, 80, 50])
    upper = np.array([130, 255, 255])

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cx, cy = None, None
        if contours:
            c = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(c)
            if area > 800:  # reduce noise
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)

        # Move a shape based on centroid; draw path if in draw mode
        if cx is not None and cy is not None:
            # Move a green square centered at centroid
            size = 30
            cv2.rectangle(frame, (cx - size, cy - size), (cx + size, cy + size), (0, 255, 0), 2)

            if draw_mode:
                path_points.append((cx, cy))

        # Draw lines across path
        for i in range(1, len(path_points)):
            cv2.line(frame, path_points[i - 1], path_points[i], (0, 255, 255), 3)

        # UI text
        cv2.putText(frame, f"Draw mode: {'ON' if draw_mode else 'OFF'} (press d to toggle, c to clear, q to quit)",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("Gesture Control Basics (Color & Contours)", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('d'):
            draw_mode = not draw_mode
        elif key == ord('c'):
            path_points.clear()
        elif key == 27 or key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
