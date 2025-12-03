import cv2

# Load the Haar Cascade for face detection

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start the webcam

cap = cv2.VideoCapture(0)

if not cap.isOpened():

  print("Error: Could not open webcam.")

  exit()

while True:

 ret, frame = cap.read()

 if not ret:

  print("Error: Failed to capture image")
  break

# Convert frame to grayscale for faster processing

 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Detect faces in the frame
 faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1, minNeighbors=5,minSize=(30, 30))

# Draw rectangles around detected faces

 for (x, y, w, h) in faces:
      cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Display the count of faces

 font = cv2.FONT_HERSHEY_SIMPLEX

 cv2.putText(frame, f'People Count: {len(faces)}', (10, 30), font, 1, (255, 0, 0), 2, cv2.LINE_AA)

# Show the result

 cv2.imshow('Face Tracking and Counting', frame)

# Quit when 'q' is pressed

 if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# Release resources

cap.release()

cv2.destroyAllWindows()
