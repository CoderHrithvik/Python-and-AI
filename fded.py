import cv2
from fer import FER

# Load emotion detector
emotion_detector = FER()

# Load OpenCV face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 
                                    "haarcascade_frontalface_default.xml")

# Start webcam
cap = cv2.VideoCapture(0)

print("Real-Time Face + Emotion Detection")
print("Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.2, 6)

    # Loop through detected faces
    for (x, y, w, h) in faces:
        # Draw face box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Crop face region
        face_region = frame[y:y + h, x:x + w]

        # Detect emotion
        emotion = emotion_detector.top_emotion(face_region)

        if emotion is not None:
            emotion_label, score = emotion
        if score is None:
            text = emotion_label
        else:
            text = f"{emotion_label} ({score:.2f})"
    else:
        text = "Unknown"

        # Display emotion label
        cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    # Show output
    cv2.imshow("Face + Emotion Detection", frame)

    # Quit on Q
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()