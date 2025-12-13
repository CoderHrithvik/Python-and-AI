# Real-Time Color Filters & Edge Detection
# Requirements: pip install opencv-python

import cv2
import numpy as np

def apply_filter(frame, mode):
    if mode == "none":
        return frame
    elif mode == "gray":
        g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)
    elif mode == "sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]], dtype="float32")
        out = cv2.transform(frame, kernel)
        return np.clip(out, 0, 255).astype(np.uint8)
    elif mode == "negative":
        return 255 - frame
    elif mode == "blur":
        return cv2.GaussianBlur(frame, (15, 15), 0)
    return frame

def apply_edges(frame, method):
    if method == "none":
        return frame
    g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if method == "canny":
        edges = cv2.Canny(g, 100, 200)
    elif method == "sobel":
        sx = cv2.Sobel(g, cv2.CV_64F, 1, 0, ksize=3)
        sy = cv2.Sobel(g, cv2.CV_64F, 0, 1, ksize=3)
        edges = cv2.convertScaleAbs(np.hypot(sx, sy))
    elif method == "laplacian":
        edges = cv2.Laplacian(g, cv2.CV_64F)
        edges = cv2.convertScaleAbs(edges)
    else:
        return frame
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    filter_mode = "none"
    edge_mode = "none"
    info = "Keys: f=cycle filter, e=cycle edges, r=reset, q/ESC=quit"

    FILTERS = ["none", "gray", "sepia", "negative", "blur"]
    EDGES = ["none", "canny", "sobel", "laplacian"]

    f_i = 0
    e_i = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)

        filtered = apply_filter(frame, FILTERS[f_i])
        edged = apply_edges(filtered, EDGES[e_i])

        cv2.putText(edged, f"Filter: {FILTERS[f_i]} | Edge: {EDGES[e_i]}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(edged, info, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

        cv2.imshow("Real-Time Filters & Edge Detection", edged)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('f'):
            f_i = (f_i + 1) % len(FILTERS)
        elif key == ord('e'):
            e_i = (e_i + 1) % len(EDGES)
        elif key == ord('r'):
            f_i, e_i = 0, 0
        elif key == 27 or key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
